#To create an environment in Confluent Cloud
resource "confluent_environment" "development" {
  display_name = "Development"

  lifecycle {
    prevent_destroy = true
  }
}


#To create a cluster in the environment
resource "confluent_kafka_cluster" "basic" {
  display_name = "servicemanagement"
  availability = "SINGLE_ZONE"
  cloud        = "AWS"
  region       = "us-east-1"
  basic {}

  environment {
    
  id=confluent_environment.development.id
  }

  lifecycle {
    prevent_destroy = true
  }
}

##To create service account

resource "confluent_service_account" "terraform_user" {
  display_name = "terraform_name_sm"
  description  = "terraform created"
}

##To assign role to the service account created
resource "confluent_role_binding" "terraform_user-kafka-cluster-admin" {
  principal   = "User:${confluent_service_account.terraform_user.id}"
  role_name   = "CloudClusterAdmin"
  crn_pattern = confluent_kafka_cluster.basic.rbac_crn
}

#To create API Key for service account
resource "confluent_api_key" "terraform_Created_APIKEY" {
  display_name = "terraform_Created_APIKEY-kafka-api-key-name"
  description  = "Kafka API Key that is owned by 'terraform_name_sm' service account"
  owner {
    id          = confluent_service_account.terraform_user.id
    api_version = confluent_service_account.terraform_user.api_version
    kind        = confluent_service_account.terraform_user.kind
  }

  managed_resource {
    id          = confluent_kafka_cluster.basic.id
    api_version = confluent_kafka_cluster.basic.api_version
    kind        = confluent_kafka_cluster.basic.kind

    environment {
     id = confluent_environment.development.id
     
    }
  }
 
}
   

# This part creates a topic 

resource "confluent_kafka_topic" "job_created" {
  kafka_cluster {
    id = confluent_kafka_cluster.basic.id
  }
  topic_name    = "job_created"
  rest_endpoint      = confluent_kafka_cluster.basic.rest_endpoint
  credentials {
    key   = confluent_api_key.terraform_Created_APIKEY.id
    secret = confluent_api_key.terraform_Created_APIKEY.secret
  }
}

resource "confluent_kafka_topic" "order_placed" {
  kafka_cluster {
    id = confluent_kafka_cluster.basic.id
  }
  topic_name    = "order_placed"
  rest_endpoint      = confluent_kafka_cluster.basic.rest_endpoint
  credentials {
    key   = confluent_api_key.terraform_Created_APIKEY.id
    secret = confluent_api_key.terraform_Created_APIKEY.secret
  }
}
  
resource "confluent_ksql_cluster" "example" {
  display_name = "example"
  csu          = 4
  kafka_cluster {
    id = confluent_kafka_cluster.basic.id
  }
  credential_identity {
    id = confluent_service_account.terraform_user.id
  }
  environment {
   id = confluent_environment.development.id 
  }
  


  lifecycle {
    prevent_destroy = true
  }
}

