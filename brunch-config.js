// See http://brunch.io for documentation.
exports.files = {
  javascripts: {
    joinTo: {
      'js/vendor.js': /^node_modules/,
      'js/index.js': /^react_app\/index/,
      'js/friends.js': /^react_app\/friends/
    }
  },
  stylesheets: {
    joinTo: {
      'css/index.css': /^react_app\/index/
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
