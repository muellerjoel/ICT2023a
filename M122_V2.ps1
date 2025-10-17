# Install the module if doesn't exist, import the module if exists

Install-Module -Name PSSQLite -Scope CurrentUser
Install-Module -Name PSUnidecode -Scope CurrentUser
Import-Module -Name PSSQLite -Scope Global
Import-Module -Name PSUnidecode -Scope Global

# Create path C:\M122

New-Item -ItemType Directory -Path "C:\M122" -Force

# Create Variable for Path of Database at C:\M122\Workers.SQLite

$Database = "C:\M122\Workers.SQLite"

# Create Variable for table WORKERS wit nessescary columns

$Query =  "CREATE TABLE IF NOT EXISTS WORKERS ( 
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Vorname TEXT NOT NULL,
    Name TEXT NOT NULL,
    Age INT CHECK(Age >= 0),
    Email TEXT NOT NULL,
    Job TEXT,
    Lohn INT CHECK(Lohn >= 0),
    Passwort TEXT NOT NULL
    )"

# SQLite will create database Workers.SQLite for us

Invoke-SqliteQuery -Query $Query -DataSource $Database


# Intialise variable to create new worker

$Vorname = ""
$Name = ""
$Age = 0
$Email = ""
$Job = ""
$Lohn = 0
$Passwort = ""

# Generate a string which is the password without random scramble
function Get-RandomCharacters($length, $characters) { 
        $random = 1..$length | ForEach-Object { Get-Random -Maximum $characters.length } 
        $private:ofs="" 
    return [String]$characters[$random]
}

# Scramble the string from Get-RandomCharacters which is the password
function Get-ScrambleString([string]$inputString){     
    $characterArray = $inputString.ToCharArray()   
    $scrambledStringArray = $characterArray | Get-Random -Count $characterArray.Length     
    $outputString = -join $scrambledStringArray
    return $outputString 
}
 

while($true) # Endless loop
{
    $Confirmation = Read-Host "Willst du einen neuen Mitarbeiter erstellen? [y/n]" # Ask question with two answewr options and save in variable
    
    if($Confirmation -eq "n"){ # Ask question if variable $Confirmation equal n
        $Exit = Read-Host "Willst du das Programm beenden? [y/n]"
    
        if($Exit -eq "y"){ # break loop when variable $Exit equal y
            break
        }
    }

    while($Confirmation -eq "y")  # While loop when variable $Confiromation equal y
    {
        $Vorname = Read-Host "Wie ist der Vorname des Mitarbeiters?"
        $Name = Read-Host "Wie ist der Nachname des Mitarbeiters?"
        $Email = $($Vorname)+"."+$($Name)+"@firma.net" # Generate E-Mailn

        $Email = $Email.ToLower() # Convert E-Mail to lowercase
        $Email = ConvertFrom-Unicode $Email # Remove Specialcharacters

        # Select table Workers an count how many times the Fullname is in the table WORKERS and save the value in variable $query
        $Query = "SELECT COUNT(*) AS ANZAHL FROM WORKERS WHERE VORNAME = '$Vorname' AND NAME = '$Name';"

        $Number = Invoke-SqliteQuery -DataSource $Database -Query $Query
        $Number = $Number -replace "@{ANZAHL=" # Remove characters which aren't necessary at the beginning
        $Number = $Number -replace "}" # Remove character at the end
        
        if($Number -ge 1){ # If number greater or equal one then add a number to the email address. If not genarate the normal email of the worker
            $Email = $($Vorname)+"."+$($Name)+$($Number)+"@firma.net"
            $Email = $Email.ToLower() # Convert E-Mail to lowercase
            $Email = ConvertFrom-Unicode $Email # Remove Specialcharacters
        }
        else{
            $Email = $($Vorname)+"."+$($Name)+"@firma.net"
            $Email = $Email.ToLower() # Convert E-Mail to lowercase
            $Email = ConvertFrom-Unicode $Email  # Remove Specialcharacters
        }

        Write-Host "Die E-Mail lautet: $($Email)" # Output the E-Mail as lowercase string

        
        while($true){
            $Age = Read-Host "Wie alt ist der Mitabeiter? Gebe eine Ganzzahl weleches dem Alter in Jahren enstpricht"
            if($Age -match '^[0-9]+$' -ne $true){ #Looks if Variable Age is a Integer
                Write-Host Gebe bitte eine Ganzzahl ein!
            }
            else{
            break
            }
        }

        
        while($true){
            $Lohn = Read-Host "Gib den Lohn von $Vorname $Name als ganzzahligen CHF-Betrag ein"
            if($Lohn -match '^[0-9]+$' -ne $true){ #Looks if Variable Lohn is a Integer
                Write-Host Gebe bitte eine Ganzzahl ein!J
            }
            else{
                break
            }
        }
        $Job  = Read-Host "Wie lautet die Jobbezeichnung vom Mitarbeiter $Vorname"$Name"?"

        # Generate a 8 characters password
        $Passwort = Get-RandomCharacters -length 5 -characters 'abcdefghiklmnoprstuvwxyz' # Get 5 characters of the lowercase alphabet
        $Passwort += Get-RandomCharacters -length 1 -characters 'ABCDEFGHKLMNOPRSTUVWXYZ' # Get one character of the uppercase alphabet
        $Passwort += Get-RandomCharacters -length 1 -characters '1234567890' # Get one digit
        $Passwort += Get-RandomCharacters -length 1 -characters '!"§$%&/()=?}][{@#*+' # Get one special character
    
        $Passwort = Get-ScrambleString $Passwort # Scramble the string with the Scramble-String function
        
        # Output of the password and workers fullname
        Write-Host "Das Passwort des Mitarbeiters $Vorname $Name ist: $Passwort"

        # Give each column in table WORKERS a variable with a value like Vorname <= Joe of the variable $Vorname
        $DataTable = 1..1 | ForEach-Object{
        [pscustomobject]@{
            Vorname = "$Vorname"
            Name = "$Name"
            Age = $Age
            Email = "$Email"
            Job = "$Job"
            Lohn = $Lohn
            Passwort = "$Passwort"
        }
    } | Out-DataTable

    #Insert the data within a single transaction (SQLite is faster this way)
    Invoke-SQLiteBulkCopy -DataTable $DataTable -DataSource $Database -Table WORKERS -NotifyAfter 1000  # -verbose (This option is only to debug)
    break
    }
}
#We have a database, and a table, let's view the table info. Here the names, age and email of the workers and finish the process
Invoke-SqliteQuery -DataSource $Database -Query "SELECT Vorname, Name, Age, Email FROM WORKERS"
exit