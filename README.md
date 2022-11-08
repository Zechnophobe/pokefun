# pokefun
 A fun little pokemon api

A simple app to deliver pokemon information to the end user. Uses pokeapi as source of truth. Caches data.
Sorry if your favorite pokemon didn't make the cut, the administration holds no responsibility for
differences of opinion.

Run with
```
python -m flask run
```

Supports two end points

```
get /favorite_pokemon
```

To get a list of MY favorite pokemon

```
get /favorite_pokemon/<name>
```

To get information about a single pokemon