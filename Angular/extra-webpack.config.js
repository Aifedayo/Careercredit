
const ProvidePlugin = require('webpack/lib/ProvidePlugin');


module.exports = {
  module: {
    rules: [
      {
        test: /\.cool$/,
        use: 'cool-loader'
      }
    ]
  },
  plugins:[
    new ProvidePlugin({
    videojs: 'video.js/dist/video.cjs.js',
    RecordRTC: 'recordrtc',
    MediaStreamRecorder: ['recordrtc', 'MediaStreamRecorder']
  })
  ],
  resolve:{
    alias: {
    videojs: 'video.js',
    WaveSurfer: 'wavesurfer.js',
    RecordRTC: 'recordrtc'
}
  }
};
