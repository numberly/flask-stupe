Cursor support
##############

Pagination
==========

Views that returns a MongoDB_ cursor can be easily paginated using the
:func:`paginate decorator <flask_stupe.pagination.paginate>`. See the
following example:

.. code-block:: python

    @app.route("/news")
    @paginate
    def get_news():
        return db.news.find()


With this setting, elements from the *news* collection will be returned. You
can control the pagination with the **skip** and **limit** query parameters.

Sorting
=======

You also get sorting using the same decorator. With the example from the
previous section, you can use the **sort** query parameter to sort on one of
the MongoDB_ fields. You can prefix the field with a minus sign to sort in
descending order.

.. _MongoDB: https://www.mongodb.com/
