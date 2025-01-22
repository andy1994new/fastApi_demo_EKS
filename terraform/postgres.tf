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

  create_db_subnet_group = true
  subnet_ids             = module.vpc.private_subnets

  vpc_security_group_ids = [module.security_group.security_group_id]

  tags = {
    Terraform   = "true"
    Environment = local.env
  }
}

# save the username and endpoint of the database in a Kubernetes secret:
resource "kubernetes_secret" "db_credentials" {
  metadata {
    name = "db-credentials"
    namespace = "default"
  }

  data = {
    username = base64encode(module.db.db_instance_username)
    endpoint = base64encode(module.db.db_instance_endpoint)
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