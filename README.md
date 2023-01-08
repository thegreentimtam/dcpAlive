# dcpAlive

Runs DCP-o-Matic with Alive Progress Bars

## Requires

Requires DCP-o-Matic CLI and FFMPEG to be installed.

## Usage

```python
from dcpAlive import dcpAlive
dcpAlive( 'input.mkv' )
```

### Parameters
`input` - the input video file
`output` - the output directory, defaults to `'.'`
`name` - the name of the film. Defaults to `False`. When `False`, uses the input filename.
`type` - the type of content. Defaults to `'FTR'`