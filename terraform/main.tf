terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.38.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# Create VPC
resource "aws_vpc" "task_manager_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "Task Manager VPC"
  }
}

# Create Public Subnet
resource "aws_subnet" "tma_public_subnet" {
  vpc_id                  = aws_vpc.task_manager_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1a"

  tags = {
    Name = "Public Subnet"
  }
}

# Create Internet Gateway
resource "aws_internet_gateway" "task_manager_igw" {
  vpc_id = aws_vpc.task_manager_vpc.id

  tags = {
    Name = "Task Manager IGW"
  }
}

# Add Route to Default Route Table
resource "aws_default_route_table" "route_table" {
  default_route_table_id = aws_vpc.task_manager_vpc.default_route_table_id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.task_manager_igw.id
  }

  tags = {
    Name = "Route Table"
  }
}

# Create Security Group for HTTP and SSH access
resource "aws_security_group" "task_manager_app_sg" {
  name        = "task_manager_app_sg"
  description = "Allow HTTP and SSH inbound traffic"
  vpc_id      = aws_vpc.task_manager_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Task Manager App Security Group"
  }
}

# Create TLS Private Key
resource "tls_private_key" "task_manager_app_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# Create AWS key pair using the generated Private Key
resource "aws_key_pair" "task_manager_app_key" {
  key_name   = "task_manager_app_key"
  public_key = tls_private_key.task_manager_app_key.public_key_openssh

  provisioner "local-exec" {
    command = "echo '${tls_private_key.task_manager_app_key.private_key_pem}' > task_manager_app_key.pem && chmod 400 task_manager_app_key.pem"
  }
}

// Create EC2 instance
resource "aws_instance" "task_manager_app" {
  ami                    = "ami-06aa3f7caf3a30282"
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.tma_public_subnet.id
  key_name               = aws_key_pair.task_manager_app_key.key_name
  vpc_security_group_ids = [aws_security_group.task_manager_app_sg.id]

  tags = {
    Name = "Task Manager App"
  }
}

// Create DynamoDB Table
resource "aws_dynamodb_table" "Tasklist" {
  name           = "Tasklist"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "TaskId"

  attribute {
    name = "TaskId"
    type = "S"
  }

  tags = {
    Name = "Task List Table"
  }


}

// Output the public IP address of the EC2 instance
output "ec2_public_ip" {
  value = aws_instance.task_manager_app.public_ip
}

