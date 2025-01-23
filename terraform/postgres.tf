module "db" {
  source = "terraform-aws-modules/rds/aws"

  identifier = "${local.db_name}-postgresql"

  create_db_option_group    = false
  create_db_parameter_group = false

  engine            = "postgres"
  engine_version    = "14"
  instance_class    = "db.t4g.micro"
  allocated_storage = 5

  db_name  = local.db_name
  username = "dbuser"
  port     = "5432"
  password = local.db_password

  create_db_subnet_group = true
  subnet_ids             = module.vpc.private_subnets

  vpc_security_group_ids = [module.security_group.security_group_id]

  tags = {
    Terraform   = "true"
    Environment = local.env
  }
}

data "aws_secretsmanager_secret" "db_password" {
  arn = module.db.db_instance_master_user_secret_arn  # ARN from your RDS module
}

data "aws_secretsmanager_secret_version" "db_password_value" {
  secret_id = data.aws_secretsmanager_secret.db_password.id
}

# Kubernetes secret to store DB credentials
resource "kubernetes_secret" "db_credentials" {
  metadata {
    name = "db-credentials"
    namespace = "default"
  }

  data = {
    # Base64 encode the username from the RDS module
    username = base64encode(module.db.db_instance_username)

    # Base64 encode the database endpoint from the RDS module
    endpoint = base64encode(module.db.db_instance_endpoint)

    # Fetch and base64 encode the password stored in Secrets Manager
    password = base64encode(
      jsondecode(data.aws_secretsmanager_secret_version.db_password_value.secret_string).password
    )

    # Base64 encode the database name
    dbname = base64encode(local.db_name)
  }
}


module "security_group" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "~> 5.0"

  name        = local.eks_name
  description = "Complete PostgreSQL example security group"
  vpc_id      = module.vpc.vpc_id

  # ingress
  ingress_with_cidr_blocks = [
    {
      from_port   = 5432
      to_port     = 5432
      protocol    = "tcp"
      description = "PostgreSQL access from within VPC"
      cidr_blocks = module.vpc.vpc_cidr_block
    },
  ]

    tags = {
    Terraform   = "true"
    Environment = local.env
  }
}