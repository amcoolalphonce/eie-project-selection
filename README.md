# EIE Project Selection System

An automated system for final year electrical project selections at the University of Nairobi.

## Features

### For Users
- **User Registration and Authentication**: Secure login system for students
- **Project Selection**: Browse and select up to 3 projects from available options
- **Project Management**: View selected projects and manage selections
- **User-Friendly Interface**: Modern, responsive design with intuitive navigation

### For Administrators
- **Manual Project Entry**: Add projects one by one through the admin interface
- **CSV Bulk Import**: Upload CSV files containing multiple projects at once
- **Multi-Format Support**: Automatically detects and supports various CSV formats
- **Project Management**: Edit, delete, and manage all projects in the system
- **User Management**: Monitor user selections and system usage

## CSV Upload Feature

### How to Use CSV Upload

1. **Access Admin Interface**: Log in as an administrator
2. **Navigate to Projects**: Go to the Projects section in the admin panel
3. **Upload CSV**: Click the "Upload CSV" button
4. **Select File**: Choose a CSV file with any supported format
5. **Import**: The system will automatically detect the format and import the data

### Supported CSV Formats

The system automatically detects and supports the following CSV formats:

#### Format 1: Standard Format
```csv
project_number,project_title
PRJ001,Smart Home Automation System
PRJ002,Solar Power Management System
PRJ003,Electric Vehicle Charging Station
```

#### Format 2: PRJ/TITLE Format
```csv
PRJ,TITLE
001,INVESTIGATE DESIGN AND OPERATIONALIZE SATELLITE TRACKING MECHANISM
002,INVESTIGATE AND DESIGN OF A MICROWAVE PATCH ANTENNA
003,INVESTIGATE AND DESIGN OF SATELLITE COMMUNICATION
```

#### Format 3: Legacy Format
```csv
prj_number,prj_title
PRJ001,Smart Home Automation System
PRJ002,Solar Power Management System
PRJ003,Electric Vehicle Charging Station
```

### CSV Import Rules

- **Automatic Format Detection**: The system automatically detects the CSV format
- **Required Data**: Both project number and title are required for each row
- **Unique Project Numbers**: Each project number must be unique
- **Duplicate Handling**: Existing projects with the same number will be updated
- **Error Reporting**: Detailed error messages for any issues during import
- **Large File Support**: Handles CSV files with hundreds of projects

## Installation and Setup

### Prerequisites
- Python 3.8+
- Django 4.0+
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd eie-project-selection-1
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

### Management Commands

#### Import Projects from CSV
```bash
python manage.py import_projects_csv path/to/your/file.csv
```

This command allows you to import projects from a CSV file via command line and supports all the same formats as the web interface.

## Usage

### For Students
1. Register for an account
2. Log in to the system
3. Browse available projects
4. Select up to 3 projects
5. View your selected projects

### For Administrators
1. Log in to the admin interface
2. Add projects manually or upload CSV files
3. Monitor user selections
4. Manage the project database

## File Structure

```
eie-project-selection-1/
├── base/                          # Main application
│   ├── models.py                  # Database models
│   ├── views.py                   # View logic
│   ├── admin.py                   # Admin interface configuration
│   ├── templates/                 # HTML templates
│   └── management/                # Management commands
│       └── commands/
│           └── import_projects_csv.py
├── users/                         # User management app
├── EIE/                          # Project settings
├── media/                        # Uploaded files
└── requirements.txt              # Python dependencies
```

## Database Models

### Project
- `project_number`: Unique identifier for the project
- `project_title`: Title/name of the project
- `created_at`: Timestamp when the project was added

### UserProjectSelection
- Links users to their selected projects
- Tracks selection timestamps
- Enforces maximum selection limit (3 projects)

### ProjectCSV
- Stores uploaded CSV files for reference
- Tracks upload timestamps

## Security Features

- **Authentication Required**: All project selection features require login
- **CSRF Protection**: All forms include CSRF tokens
- **Input Validation**: Comprehensive validation for all user inputs
- **Admin Access Control**: Restricted admin interface access

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For support or questions, contact: gevira@uonbi.ac.ke
