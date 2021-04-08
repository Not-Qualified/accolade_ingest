class model(db.Model):
	url = db.Column(db.String, unique=True, nullable=False, primary_key=True, )
	cache_ttl = db.Column(db.Integer, nullable=False, )
	cache_grace = db.Column(db.Integer, nullable=False, )
	status = db.Column(db.Integer,  nullable=False, )
	response_time = db.Column(db.Float,  nullable=False, )
	cache_state = db.Column(db.Boolean, default=True,  nullable=True, )
	sitemap = db.Column(db.String, nullable=True, )