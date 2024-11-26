import request from "request";
import sqlite from "sqlite3";
import xlsx from "xlsx";

const database_path = "./database.db";
const table_name = "radusuarios";
const create_new_table = true;
const token =
  "123:1126d710b86bd9344315e13133abe8cf722bcb88321203ab5d9e201475658f54";

const sqlite3 = sqlite.verbose();
const db = new sqlite3.Database(database_path, (err) => {
  if (err) {
    return console.log("Erro ao conectar o Banco de Dados:", err.message);
  }

  console.log("Conectado ao Banco de Dados.");
});

let options = {
  method: "GET",
  url: "https://ixc.opponet.com.br/webservice/v1/radusuarios",
  headers: {
    "Content-Type": "application/json",
    Authorization: "Basic " + new Buffer.from(token).toString("base64"),
    ixcsoft: "listar",
  },
  body: {
    qtype: "radusuarios.id",
    query: "0",
    oper: ">",
    page: "1",
    rp: "100000",
    sortname: "radusuarios.id",
    sortorder: "asc",
  },
  json: true,
};

request(options, function (error, response, body) {
  if (error) throw new Error(error);
  let registros = body.registros;

  // Criação da Tabela
  let create_new_table_command = `CREATE TABLE IF NOT EXISTS ${table_name} (`;

  if (create_new_table) {
    for (let item in registros[0]) {
      create_new_table_command += `${item} TEXT,`;
    }
    create_new_table_command = create_new_table_command.slice(0, -1);
    create_new_table_command += `)`;

    db.run(create_new_table_command, (err) => {
      if (err) {
        return console.log("Erro ao Criar a Tabela:", err.message);
      } else {
        console.log("Tabela Criada com Sucesso.");
      }
    });
  }

  // Inserção dos Dados na Tabela
  for (let registro of registros) {
    let add_new_client_command = `INSERT INTO ${table_name} VALUES (`;

    for (let value in registro) {
      add_new_client_command += `'${registro[value]}',`;
    }
    add_new_client_command = add_new_client_command.slice(0, -1);
    add_new_client_command += ")";
    console.log(add_new_client_command);
    db.run(add_new_client_command, function (err) {
      if (err) {
        console.error("Erro ao inserir dados:", err.message);
      } else {
        console.log(
          `Usuário ${registro.razao} inserido com sucesso, ID: ${this.lastID}`
        );
      }
    });
  }
});
