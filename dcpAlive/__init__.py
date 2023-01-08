import os
import subprocess
import random
import string
from time import sleep
from alive_progress import alive_bar
import shutil
import ffAlive

def getRandomString( length ):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def takeClosest(myList: list, myNumber: int or float) -> int:
    closest = myList[0]
    for i in range(1, len(myList)):
        if abs(myList[i] - myNumber) < abs(closest - myNumber):
            closest = myList[i]
    return closest

def getDAR( file ):
    metadata = ffAlive.ffprobe( file )
    if 'streams' in metadata:
        for stream in metadata['streams']:
            if ( 'codec_type' in stream and stream['codec_type'] == 'video' ):
                if 'sample_aspect_ratio' in stream:
                    sar = stream['sample_aspect_ratio'].split(":")
                    sar = int(sar[0]) / int(sar[1])
                else:
                    sar = 1
                width = int( stream['width'] )
                height = int( stream['height'] )
                return width / height * sar
    return 0

def getDur( file ) -> float:
    """Gets the duration in seconds of a file"""
    metadata = ffAlive.ffprobe( file )
    if 'format' in metadata and 'duration' in metadata['format']:
        return float( ffAlive.ffprobe( file )['format']['duration'] )
    return 0

def checkIsVideo( file ):
    metadata = ffAlive.ffprobe( file )
    if 'streams' in metadata:
        for stream in metadata['streams']:
            if ( 'codec_type' in stream and stream['codec_type'] == 'video' ):
                return True
    return False 

def findClosestContainer( file ):
    if not checkIsVideo( file ):
        return 185
    return takeClosest( [ 185, 239 ], getDAR( file ) * 100 )

def getDCPAudio( project ) -> str:
    """Gets the in progress audio file during DCP creation."""
    while True:
        for filename in os.listdir( project ):
            if( os.path.splitext( filename )[1] == '.mxf' ):
                return os.path.join ( project, filename )
        sleep( 0.5 )

def dcpAlive( input, output = '.', name = False, type = 'FTR' ):
    project = getRandomString( 40 )
    if name == False:
        name = os.path.basename( input )
    subprocess.call( [
        'dcpomatic2_create',
        '-o', project,
        '--container-ratio', str( findClosestContainer( input ) ),
        '-c', type,
        '-n', name,
        input
    ] )
    dcpProcess = subprocess.Popen([
        'dcpomatic2_cli',
        '-n', '-d',
        project
    ], stdout=subprocess.PIPE )
    audio = getDCPAudio( project )
    estimatedSize = round ( ( getDur( input ) + 1 ) * 864000 )
    with alive_bar( ffAlive.getTotal( input ), manual=True ) as bar:
        while( os.path.exists( audio ) ):
            try:
                bar( os.path.getsize( audio ) / estimatedSize )
            except:
                pass # This try/except exists in case the file is deleted in between checking if exists, and checking size
            sleep( 2 )
        path = dcpProcess.stdout.read().strip().decode("utf-8")
        shutil.move( path, os.path.join( output, os.path.basename( path ) ) )
        bar( 1 )
    shutil.rmtree( project )
