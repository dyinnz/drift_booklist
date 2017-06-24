// See http://brunch.io for documentation.
exports.files = {
  javascripts: {
    joinTo: {
      'js/vendor.js': /^(?!react_app)/,
      'js/app.js': /^react_app/
    }
  },
  stylesheets: {joinTo: 'css/app.css'}
};

exports.plugins = {
  babel: {presets: ['latest', 'react']}
};

exports.paths = {
  public: 'static/react',
  watched: ['react_app']
};
