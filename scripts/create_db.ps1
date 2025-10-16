param(
    [string]$DbHost = "localhost",
    [int]$Port = 5432,
    [string]$AdminUser = "postgres",
    [string]$AdminPassword = "",
    [string]$DbName = "flask_blog",
    [string]$AppUser = "flaskuser",
    [string]$AppPassword = "flaskpass"
)

$ErrorActionPreference = "Stop"

Write-Host "Creating PostgreSQL database '$DbName' and user '$AppUser' on ${DbHost}:${Port}..."

if ($AdminPassword -ne "") {
  $env:PGPASSWORD = $AdminPassword
} else {
  if ($env:PGPASSWORD -eq $null -or $env:PGPASSWORD -eq "") {
    Write-Host "Admin password not provided. Set -AdminPassword or PGPASSWORD env var."
    exit 1
  }
}

# Create database, role and grant privileges with separate commands
& psql -h $DbHost -p $Port -U $AdminUser -d postgres -v ON_ERROR_STOP=1 -c "CREATE DATABASE $DbName;"
try {
  & psql -h $DbHost -p $Port -U $AdminUser -d postgres -v ON_ERROR_STOP=1 -c "CREATE ROLE $AppUser LOGIN PASSWORD '$AppPassword';"
} catch {
  Write-Host "Role may already exist, continuing..."
}
& psql -h $DbHost -p $Port -U $AdminUser -d postgres -v ON_ERROR_STOP=1 -c "GRANT ALL PRIVILEGES ON DATABASE $DbName TO $AppUser;"

Write-Host "Done. Configure DATABASE_URL as: postgresql+psycopg://${AppUser}:${AppPassword}@${DbHost}:${Port}/$DbName"

