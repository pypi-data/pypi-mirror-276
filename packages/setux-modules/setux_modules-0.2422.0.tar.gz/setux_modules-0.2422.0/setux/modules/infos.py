from setux.core import __version__
from setux.core.module import Module
from setux.logger import info


class Distro(Module):
    '''Show target infos
    '''

    def python_version(self, target):
        ret, out, err = target.run('python -V')
        if ret == 0:
            version = out[0]
        else:
            ret, out, err = target.run('python3 -V')
            version = out[0] if ret == 0 else '- -'
        version = version.split()[1]
        return version

    def deploy(self, target, **kw):
        kernel = target.kernel
        python = self.python_version(target)
        addr = target.net.addr or '!'

        infos = f'''
        target : {target}
        distro : {target.distro.name}
        python : {python}
        kernel : {kernel.name} {kernel.version} / {kernel.arch}
        user   : {target.login.name}
        host   : {target.system.hostname}
        addr   : {addr}
        setux  : {__version__}
        '''

        info(infos)
        return True
