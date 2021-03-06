'use strict';

import api from './api';

export default {
    find: function(project_id, callback) {
        api().get('/api/project/' + project_id, callback);
    },

    search: function (isPublic, userId, offset, limit, filter, callback) {
        let queryString = 'user_id=' + userId +
            '&offset=' + offset +
            '&limit=' + limit +
            '&filter=' + filter;

        if (isPublic !== null) queryString += '&is_public=' + isPublic;

        let url = '/api/projects?' + queryString;

        api().get(url, callback);
    }
}