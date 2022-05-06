var geotiff2json = require('weacast-gtiff2json'),
fs = require('fs')

geotiff2json('GCBM_Demo_Run/layers/tiled/classifiers/Classifier1_moja.tiff', true).then(function(data) {
  fs.writeFile('data.json', JSON.stringify(points), function(err) {
    if(err) {
      console.error('Oh no, writing failed!', err)
      return
    }
    console.log('wrote ' + (data.length / 2) + ' tuples into file.')
})})