
# decorator
def rest_call(http_method):
    def outer(func):
        def inner(self, *args, **kwargs):
            method, params, data = func(self, *args, **kwargs)

            if   http_method=='delete': sess_func=self.session.delete
            elif http_method=='get'   : sess_func=self.session.get
            elif http_method=='post'  : sess_func=self.session.post
            elif http_method=='put'   : sess_func=self.session.put
            else:
                raise WattleError("Invalid HTTP Method")

            url = base_URL + method

            response self_func(url, params=params, json=data)
            


            self.logger.debug('Request URL: {0}'.format(response.request.url))
            self.logger.debug('Response Code: {0}'.format(response.status_code))
            self.lastCall = response
            self.history.append(response)

            # Handle non-200 responses
            if response.status_code != 200:
                raise WattleError(response)
            
            try:
                data = response.json()
                self.logger.debug('Response Body: {}'.format(json.dumps(data, indent=2, sort_keys=True)))
            except Exception:
                data = response.content
                self.logger.debug('Response Body: {}'.format(data))
            return data
        return inner
    return outer