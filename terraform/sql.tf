resource "azurerm_mssql_server" "main" {
  name                         = "${var.project_name}-sql"
  resource_group_name          = azurerm_resource_group.main.name
  location                     = azurerm_resource_group.main.location
  version                      = "12.0"
  administrator_login          = var.sql_admin_username
  administrator_login_password = var.sql_admin_password
}

resource "azurerm_mssql_database" "main" {
  name                        = "metrics"
  server_id                   = azurerm_mssql_server.main.id
  sku_name                    = "GP_S_Gen5_1"
  min_capacity                = 0.5
  auto_pause_delay_in_minutes = 60
}

resource "azurerm_mssql_firewall_rule" "aks_outbound" {
  name             = "AllowAKSOutboundIP"
  server_id        = azurerm_mssql_server.main.id
  start_ip_address = "132.196.122.86"
  end_ip_address   = "132.196.122.86"
}

resource "azurerm_mssql_firewall_rule" "allow_azure_services" {
  name             = "AllowAllWindowsAzureIps"
  server_id        = azurerm_mssql_server.main.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}
