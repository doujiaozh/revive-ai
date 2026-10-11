const os = require('os');
os.hostname = function () { return 'localhost'; };