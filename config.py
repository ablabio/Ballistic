import argparse
import json

# read arguments.
parser = argparse.ArgumentParser()
parser.add_argument('--symbols_path', help='path to file containing stock symbols to subscribe to.')
args = parser.parse_args()
symbols_path = args.symbols_path

# import symbols
symbols_file = open(symbols_path, "r")
symbols = symbols_file.read().split('\n')
symbols_file.close()

# export config files

for i in range(len(symbols)):
	sym = symbols[i]
	cmd = "python3 stock_subscription.py --symbol " + sym
	config_json = (
"""
module.exports = {
  apps : [{
    name: 'stock_subscription_""" + sym + """',
    cmd: '"""+ cmd +
    """',
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'development'
    },
    env_production: {
      NODE_ENV: 'production'
    }
  }],
  deploy : {
    production : {
      user : 'node',
      host : '212.83.163.1',
      ref  : 'origin/master',
      repo : 'git@github.com:repo.git',
      path : '/var/www/production',
      'post-deploy' : 'npm install && pm2 reload ecosystem.config.js --env production'
    }
  }
};
"""
	)
	config_file = open("./pm2_configs/config_" + sym + ".js", "w")
	config_file.write(config_json)
	config_file.close()
