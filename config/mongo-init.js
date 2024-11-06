db.createUser(
  {
    user: "admin",
    pwd: "P@$$w0rd", // or cleartext password
    roles: [
      { role: "userAdminAnyDatabase", db: "admin" },
      { role: "readWriteAnyDatabase", db: "admin" }
    ]
  }
)