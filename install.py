import subprocess
import os.path
import os

osName = os.name
isWindows = os.name == 'nt'

ONLY_NUMPY = 'numpy'
BOTH = 'both'
NEITHER = 'neither'

def testNumpy():
    try:
        import numpy
        return True
    except:
        return False

def testMatplotlib():
    try:
        import matplotlib
        return True
    except:
        return False

def testImports():
    numpy = testNumpy()
    matplot = testMatplotlib()
    if numpy and matplot: return BOTH
    if numpy: return ONLY_NUMPY
    return NEITHER 

def installNumpy(installerPath):
    print '(1/ 2) Installing numpy:'
    if isWindows:
        subprocess.call(['python', installerPath, 'install', 'numpy==1.6.2'])
    else:
        print 'You may have to log in. If prompted, enter the password for this computer.'
        subprocess.call(['sudo', 'python', installerPath, 'install', 'numpy==1.6.2'])
    print ''

def installMatplotlib(installerPath):
    print '(2/ 2) Installing matplotlib'
    if isWindows:
        subprocess.call(['python', installerPath, 'install', 'matplotlib'])
    else:
        print 'You may have to log in. If prompted, enter the password for this computer.'
        subprocess.call(['sudo', 'python', installerPath, 'install', 'matplotlib'])
    print ''

def easyInstallNumpy(installerPath):
    print '(1/ 2) Installing numpy:'
    if isWindows:
        subprocess.call(['python', installerPath, 'numpy'])
    else:
        print 'You may have to log in. If prompted, enter the password for this computer.'
        subprocess.call(['sudo', 'python', installerPath, 'numpy'])
    print ''

def easyInstallMatplotlib(installerPath):
    print '(2/ 2) Installing matplotlib'
    if isWindows:
        subprocess.call(['python', installerPath, 'matplotlib'])
    else:
        print 'You may have to log in. If prompted, enter the password for this computer.'
        subprocess.call(['sudo', 'python', installerPath, 'matplotlib'])
    print ''

def pipInstall(status):
    pluginDir = 'plugins'
    pipRootDir = os.path.join(pluginDir, 'pip')
    pipDir = os.path.join(pipRootDir, 'pip')
    installPath = os.path.join(pipDir, 'runner.py')
    if status == NEITHER:
        installNumpy(installPath)
    installMatplotlib(installPath)

def easyInstall(status):
    pluginDir = 'plugins'
    setupToolsDir = os.path.join(pluginDir, 'setuptools')
    easyInstallPath = os.path.join(setupToolsDir, 'easy_install.py')
    if status == NEITHER:
        easyInstallNumpy(easyInstallPath)
    easyInstallMatplotlib(easyInstallPath)

def run():
    print '-----------------------------------------'
    print 'Welcome to the CS221 project 3 installer.'
    print 'In order to make your project easier to program,'
    print 'and to allow you to visualize what you are doing'
    print 'we are going to use some basic python tools:'
    print 'numpy and matplot lib.'
    print '-----------------------------------------'
    print ''

    status = testImports()

    if status == BOTH:
        print 'It looks like you have everything installed.'
        print 'Good luck with the assignment.'
        return
    if status == ONLY_NUMPY:
        print 'It looks like you only have numpy installed.'
        print 'We are going to try and install matplotlib.'
        print 'But know that it is not essential to the assignment.'
    raw_input("Press Enter to continue:")
    print ''
    
    
    easyInstall(status)

    status = testImports()

    if status != BOTH:
        print 'Well that didn\'t work. Let\'ts try this...'
        print ''
        pipInstall(status)

    status = testImports()

    print '-----------------------------------------'
    if status == BOTH:
        print 'It looks like you have everything installed.'
        print 'Good luck with the assignment.'
    if status == ONLY_NUMPY:
        print 'It looks like we successfully installed numpy,'
        print 'but were unable to install matplotlib.'
        print 'Matplotlib is not essential to the assignment.'
        print 'Send the log of this script to the CS221 staff,'
        print 'and we will investigate!'
    if status == NEITHER:
        print 'Oh no! We were not able to install either numpy OR'
        print 'matplot lib (numpy is more essential). Email the'
        print 'transcript of this run to the staff list right now,'
        print 'and we will help you figure out how to move forward.'
        print 'In the mean time you can use the corn machines to'
        print 'develop your solution.'
    print '-----------------------------------------'

if __name__ == "__main__":
    run()


