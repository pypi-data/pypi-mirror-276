import atomacos
import psutil
from pydantic import BaseModel
from AppKit import NSWorkspace


class ApplicationBundle(BaseModel):
    pid: int
    bundle_id: str
    name: str
    cmdline: str


class BundleManager:
    def _get_bundle_id(self, pid: int):
        running_apps = NSWorkspace.sharedWorkspace().runningApplications()
        for app in running_apps:
            if app.processIdentifier() != pid:
                continue
            app_ref = atomacos.getAppRefByPid(pid)
            if len(app_ref.windows()) == 0:
                return None
            return app.bundleIdentifier()
        return None

    def list_bundles(self):
        """
        >>> bm = BundleManager()
        >>> bm.list_bundles()
        """
        my_owner = psutil.Process().username()
        print('Listing bundles...')
        processes = psutil.process_iter(['pid', 'name', 'cmdline', 'username'])
        application_bundles = []
        for process in processes:
            try:
                if my_owner != process.username():
                    continue
                bundle_id = self._get_bundle_id(process.pid)
                if bundle_id is None:
                    continue
                application_bundles.append(ApplicationBundle(pid=process.pid,
                                                             bundle_id=bundle_id,
                                                             name=process.name(),
                                                             cmdline=' '.join(process.cmdline())))
            except psutil.AccessDenied:
                continue
            except psutil.ZombieProcess:
                continue
        return application_bundles

    def find_all_bundles(self, query: list[str]):
        bundles = self.list_bundles()
        found_bundles = []
        for bundle in bundles:
            if bundle.bundle_id in query:
                found_bundles.append(bundle)
        return found_bundles
