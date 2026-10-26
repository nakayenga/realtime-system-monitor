resource "azurerm_eventhub_namespace" "main" {
  name                = "${var.project_name}-ehns"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "Standard"
  capacity            = 1
}

resource "azurerm_eventhub" "metrics" {
  name              = "system-metrics"
  namespace_id      = azurerm_eventhub_namespace.main.id
  partition_count   = 4
  message_retention = 1
}

resource "azurerm_eventhub" "dlq" {
  name              = "system-metrics-dlq"
  namespace_id      = azurerm_eventhub_namespace.main.id
  partition_count   = 4
  message_retention = 1
}
