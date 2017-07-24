// http://eslint.org/docs/user-guide/configuring

module.exports = {
  root: true,
  parser: 'babel-eslint',
  parserOptions: {
    sourceType: 'module'
  },
  env: {
    browser: true,
  },
  // https://github.com/feross/standard/blob/master/RULES.md#javascript-standard-style
  extends: 'standard',
  // required to lint *.vue files
  plugins: [
    'html'
  ],
  // add your custom rules here
  'rules': {
    // allow paren-less arrow functions
    'arrow-parens': 0,
    // allow async-await
    'generator-star-spacing': 0,
    // allow debugger during development
    'no-debugger': process.env.NODE_ENV === 'production' ? 2 : 0,
    // do not require camel case
    "camelcase": [0],
    "space-before-function-paren": [0],
    "space-before-blocks": [0],
    "no-useless-escape": [0],
    "eqeqeq": [0],
    "no-unused-vars": [0],
    "brace-style": [0],
    "no-trailing-spaces": [0],
    "no-unmodified-loop-condition": [0]
  }
}