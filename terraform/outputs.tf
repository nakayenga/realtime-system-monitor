output "resource_group_name" {
  value = azurerm_resource_group.main.name
}

output "eventhub_namespace" {
  value = azurerm_eventhub_namespace.main.name
}

output "acr_login_server" {
  value = azurerm_container_registry.main.login_server
}

output "aks_name" {
  value = azurerm_kubernetes_cluster.main.name
}

output "sql_server_fqdn" {
  value = azurerm_mssql_server.main.fully_qualified_domain_name
}
