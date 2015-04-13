#!/usr/bin/env python

from pigeon import app
app.run(debug=app.config.get('DEBUG', False),
        host='0.0.0.0',
        port=5654)
