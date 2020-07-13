const path = require('path');

module.exports = {
  mode: 'development',
  entry: './jidp2/js/main.jsx',
  output: {
    path: path.join(__dirname, '/jidp2/static/js/'),
    filename: 'bundle.js',
  },
  module: {
    rules: [
      {
        // Test for js or jsx files
        test: /\.jsx?$/,
        loader: 'babel-loader',
        options: {
          presets: ['@babel/preset-env', '@babel/preset-react'],
        },
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },
};
