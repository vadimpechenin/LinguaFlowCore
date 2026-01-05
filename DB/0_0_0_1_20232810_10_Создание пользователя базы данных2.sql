do $$
begin

    CREATE USER lfcuser WITH ENCRYPTED PASSWORD 'a_vEry_dIfdfIc$ul12t_pA45s$sWord';
    GRANT CONNECT ON DATABASE lfc TO lfcuser;
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO lfcuser;

    raise info 'Работа успешно завершена!';
exception when others 
then
    rollback;
    raise notice 'ERROR CODE: %. MESSAGE TEXT: %', SQLSTATE, SQLERRM;
end;
$$
