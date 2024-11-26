import sqlite from "sqlite3";

const sqlite3 = sqlite.verbose();

const db = new sqlite3.Database("./database.db");

async function get_database_info(table, column_name, name) {
  const query = `SELECT * FROM ${table} WHERE ${column_name} = '${name}'`;
  db.all(query, (err, rows) => {
    if (err) {
      console.error(err.message);
      return;
    }
    console.log(rows);
  });
}

get_database_info("clientes", "razao", "LUCIANA LIMA FARIAS");
