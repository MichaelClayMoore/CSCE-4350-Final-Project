CREATE OR REPLACE FUNCTION public.store_add_user(email text, password text, admin text)
    RETURNS void
    LANGUAGE 'plpython3u'
	AS $BODY$
	
	add_user_to_user_table = 'INSERT INTO users(email,password,admin) VALUES(\'' + email + '\',\''+ password + '\',' + admin +'::boolean )'
	plpy.execute(add_user_to_user_table)
	
	make_cart_for_user = 'INSERT INTO carts(user_id) (SELECT user_id from users where email = \''+ email +'\')'
	plpy.execute(make_cart_for_user)
	
	$BODY$;

ALTER FUNCTION public.store_add_user(text, text, text)
    OWNER TO postgres;

--create extension plpython3u
