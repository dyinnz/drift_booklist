// See http://brunch.io for documentation.
exports.files = {
  javascripts: {
    joinTo: {
      'js/vendor.js': /^node_modules/,
      'js/index.js': /^react_app\/index/,
      'js/friends.js': /^react_app\/friends/,
      'js/mine.js': /^react_app\/mine/
    }
  },
  stylesheets: {
    joinTo: {
      'css/index.css': /^react_app\/index/,
      'css/friends.css': /^react_app\/friends/,
      'css/mine.css': /^react_app\/mine/
    }
  }
};

exports.plugins = {
  babel: {presets: ['latest', 'react']}
};

exports.paths = {
  public: 'static/react',
  watched: ['react_app']
};

exports.modules = {
  nameCleaner: path => path.replace(/^react_app\//, '')
};
