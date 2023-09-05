variable "confluent_cloud_api_key" {
  description = "Confluent Cloud API Key"
  type        = string
  default = ""   #Add the Confluent Cloud API Key
}

variable "confluent_cloud_api_secret" {
  description = "Confluent Cloud API Secret"
  type        = string
  sensitive   = true
  default = ""    #Add the Confluent Cloud API secret
}

variable "mongo_host" {
  description = "Atlas Host"
  type        = string
  sensitive   = true
  default = ""    #Provide the hostname
}

variable "mongo_username" {
  description = "MongoDB Atlas Username"
  type        = string
  sensitive   = true
  default = ""    # provide your username
}

variable "mongo_password" {
  description = "MongoDB Atlas Password"
  type        = string
  sensitive   = true
  default = ""    # Add your password
}