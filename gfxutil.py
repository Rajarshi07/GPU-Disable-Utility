import subprocess,sys
from pprint import  pprint as print

def runCMD( cmd ):
    startupinfo = subprocess.STARTUPINFO()     
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW   # prevents powershell from showing up momentarily while executing script
    runner = subprocess.run( ["powershell", "-Command", cmd], capture_output = True, stdin = subprocess.DEVNULL, startupinfo = startupinfo )
    print( runner.stdout.decode( 'UTF-8' ) )
    return runner


disable = lambda id :  runCMD( f'pnputil /disable-device "{id}"' )
enable = lambda id :  runCMD( f'pnputil /enable-device "{id}"' )
enumerate = lambda : runCMD( f'pnputil /enum-devices /class Display' )


def parseDisplays( output ):
    ## todo: fix parser removing spaces within company names in output.
    k = output.stdout.decode( 'UTF-8' ).split( '\r\n\r\n' )[1:-1]
    a = []
    for i in k:
        a.append( dict( item.split( ":" ) for item in i.replace( ' ', '' ).split( '\r\n' ) ) )
    print( f'Devices found: { len( a ) }' )
    print( a )
    return a


def getDisplays():
    completed = enumerate()
    if completed.returncode != 0:
        return None
    else:
        return parseDisplays( completed )
