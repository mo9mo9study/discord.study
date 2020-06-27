const sqlite = require("sqlite3").verbose();
const db = new sqlite.Database(
  "/home/ec2-user/sqlite3/mokumoku_online_studyroom.sqlite3"
);

const select_all = () => {
  db.each("SELECT * FROM mem_time;", (error, row) => {
    if (error) {
      console.error("Error!", error);
      return;
    }
    console.log(row);
  });
};
db.serialize(() => {
  select_all();
});

db.close();
