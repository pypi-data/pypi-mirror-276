import os
import shutil
import pkgutil
import importlib
from types import ModuleType
from typing import Any, Callable, Iterable, Type
from jinja2 import FileSystemLoader
from jinja2 import Environment
from injector_collections.CollectionItem import CollectionItem
import injector_collections
from importlib import util
from pathlib import Path

class Generator:
    generatedCollectionsDirName = 'generated'
    collectionTemplateFilename = 'collection.jinja'
    def generate(
            self,
            inject: Callable,
            collectionModule: str,
            scannedModules: Iterable[str]
            ):
        collectionModuleDirectory = self.getModuleDirectory(collectionModule)

        generatedDirPath = f'{collectionModuleDirectory}/{self.generatedCollectionsDirName}'
        shutil.rmtree(generatedDirPath, ignore_errors=True)
        os.makedirs(generatedDirPath, exist_ok=True)

        collectionModuleName = self.getModuleName(collectionModule)

        # we must import the stubs to the generated module, since later on,
        # there may be imports like: "from path.to.generated import xyz" in
        # files which contain the @CollectionItem decorator, which will be
        # imported by gatherCollectionMetadata. This can happen, if a
        # collection item itself uses a collection.
        with open(f'{generatedDirPath}/__init__.py', 'w') as f:
            f.write(f"from {collectionModuleName}.stubs import *\n")

        collectionMetadata = self.gatherCollectionMetadata(scannedModules)

        # create each collection in a seperate '<CollectionName>.py' file
        for collectionType, collectionItems in collectionMetadata.items():
            generatedFilePath = f'{generatedDirPath}/{collectionType.__name__}.py'
            with open(generatedFilePath, 'w') as f:
                f.write(self.renderCollectionTemplate(
                    inject,
                    collectionType,
                    collectionItems))

        # import every generated collection into the 'generated'-Module
        with open(f'{generatedDirPath}/__init__.py', 'w') as f:
            for file in os.listdir(generatedDirPath):
                filepath = f'{generatedDirPath}/{file}'
                if os.path.isfile(filepath) and file != '__init__.py':
                    moduleClass = Path(filepath).stem
                    moduleName = f'{collectionModuleName}.generated.{moduleClass}'
                    f.write(f"from {moduleName} import {moduleClass}\n")

    def getModuleDirectory(self, module: str|ModuleType) -> str:
        if isinstance(module, str):
            moduleSpec = util.find_spec(module)
            modulePath = moduleSpec.origin
        else:
            modulePath = module.__file__
        assert(modulePath is not None)
        return os.path.dirname(modulePath)

    def getModuleName(self, module: str|ModuleType) -> str:
        if isinstance(module, str):
            return module
        else:
            return module.__name__

    def renderCollectionTemplate(
            self,
            inject: Callable,
            collection: Type,
            collectionItems: list[tuple[Any, Any]]):
        icModuleDirectory = self.getModuleDirectory(injector_collections)
        file_loader = FileSystemLoader(f'{icModuleDirectory}')
        env = Environment(loader=file_loader)
        template = env.get_template(self.collectionTemplateFilename)
        return template.render(
            collection = collection,
            collectionItems = collectionItems,
            inject = inject
            )

    def gatherCollectionMetadata(
            self,
            scannedModules: Iterable[str],
            ) -> dict[Type, list[tuple[Any, Any]]]:
        ''' Gather Metadata for Collection generation with template

        Recursively walks through all modules in 'scannedModules' and gathers
        metadata for every class decorated with '@CollectionItem'.
        '''
        for m in scannedModules:
            for spec in self.walkModules(m):
                with open(spec.origin, 'r') as f:
                    if '@CollectionItem' in f.read():
                        importlib.import_module(spec.name)

        return CollectionItem.getItems()

    def walkModules(self, rootModule: str):
        info = util.find_spec(rootModule)
        yield info

        if info.submodule_search_locations is None:
            return

        #for modinfo in pkgutil.walk_packages(info.submodule_search_locations):
        for modinfo in pkgutil.iter_modules(info.submodule_search_locations):
            name = f'{info.name}.{modinfo.name}'
            yield util.find_spec(name)
            submods = self.walkModules(name)
            next(submods) # remove the root, which was just yielded
            for mi in submods:
                yield mi
