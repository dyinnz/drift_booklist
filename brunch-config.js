// See http://brunch.io for documentation.
exports.files = {
  javascripts: {
    joinTo: {
      'js/vendor.js': /^node_modules/,
      'js/index.js': /^react_app\/index/,
      'js/friends.js': /^react_app\/friends/,
      'js/mine.js': /^react_app\/mine/,
      'js/settings.js': /^react_app\/settings/
    }
  },
  stylesheets: {
    joinTo: {
      'css/index.css': /^react_app\/index/,
      'css/friends.css': /^react_app\/friends/,
      'css/mine.css': /^react_app\/mine/,
      'css/settings.css': /^react_app\/settings/
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
