const USE_FIX = true;
module.exports = function override(config, env) {
    if(!USE_FIX) {
    return config;
  }

  config.module.rules[1].oneOf = config.module.rules[1].oneOf.map(rule => {
    if(rule.type !== 'asset/resource') {
      return rule;
    }

    return {
      ...rule,
      exclude: [
        ...rule.exclude, /node_modules(\\|\/)three/
      ]
    }
  });

  return config;
}