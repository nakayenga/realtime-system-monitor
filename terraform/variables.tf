variable "location" {

  type = string

  default = "centralus"
}


variable "project_name" {

  type = string

  default = "realtimemetrics"
}


variable "sql_admin_username" {

  type = string

  sensitive = true
}


variable "sql_admin_password" {

  type = string

  sensitive = true
}