#!/usr/bin/env python3
"""
Comprehensive RES Setup for Alhoty App
=====================================

This script creates a complete, permanent setup for RES users to work seamlessly
with the alhoty app on top of the NDT isolation layer.

Run this once after installing both NDT and alhoty apps.
"""

import frappe
from frappe import _

def setup_res_access():
    """Complete setup for RES access to alhoty app"""
    
    print("🚀 Setting up RES access for Alhoty app...")
    
    # 1. Populate Res Access Config with all alhoty doctypes
    setup_res_whitelist()
    
    # 2. Create Res Home workspace
    setup_res_workspace()
    
    # 3. Ensure all roles exist
    setup_res_roles()
    
    # 4. Verify permissions
    verify_permissions()
    
    # 5. Clear caches
    clear_caches()
    
    print("✅ RES setup complete! Users should log out and back in.")

def setup_res_whitelist():
    """Add all alhoty doctypes to Res Access Config whitelist"""
    
    print("📋 Setting up Res Access Config whitelist...")
    
    # All alhoty doctypes that RES users need access to
    alhoty_doctypes = [
        'Branch Master',
        'Client Master', 
        'Equipment Master',
        'Material Master',
        'Project Master',
        'Work Order',
        'MT Inspection',
        'MT Inspection Result',  # Child table - explicit entry for safety
        'ToDo',  # Common Frappe doctype
        'Note',  # Common Frappe doctype
        'File',  # For attachments
        'Comment'  # For comments
    ]
    
    try:
        config = frappe.get_single('Res Access Config')
        
        # Get existing doctypes to avoid duplicates
        existing = {row.doctype_name for row in config.allowed_doctypes}
        
        # Add new doctypes
        added = []
        for doctype_name in alhoty_doctypes:
            if doctype_name not in existing:
                config.append('allowed_doctypes', {'doctype_name': doctype_name})
                added.append(doctype_name)
        
        if added:
            config.save()
            print(f"   ✓ Added {len(added)} doctypes to whitelist")
            for dt in added:
                print(f"     - {dt}")
        else:
            print("   ✓ All doctypes already in whitelist")
            
    except Exception as e:
        print(f"   ❌ Error setting up whitelist: {str(e)}")
        raise

def setup_res_workspace():
    """Create Res Home workspace with shortcuts to alhoty doctypes"""
    
    print("🏠 Setting up Res Home workspace...")
    
    workspace_data = {
        'doctype': 'Workspace',
        'name': 'Res Home',
        'title': 'Res Home',
        'icon': 'home',
        'indicator_color': 'blue',
        'is_published': 1,
        'module': 'Al Hoty',
        'public': 1,
        'content': '''[
    {
        "type": "header",
        "data": {
            "text": "Al Hoty NDT Management",
            "col": 12
        }
    },
    {
        "type": "shortcut",
        "data": {
            "shortcut_name": "Work Order",
            "col": 3
        }
    },
    {
        "type": "shortcut", 
        "data": {
            "shortcut_name": "MT Inspection",
            "col": 3
        }
    },
    {
        "type": "shortcut",
        "data": {
            "shortcut_name": "Equipment Master",
            "col": 3
        }
    },
    {
        "type": "shortcut",
        "data": {
            "shortcut_name": "Client Master", 
            "col": 3
        }
    },
    {
        "type": "header",
        "data": {
            "text": "Master Data",
            "col": 12
        }
    },
    {
        "type": "shortcut",
        "data": {
            "shortcut_name": "Branch Master",
            "col": 4
        }
    },
    {
        "type": "shortcut",
        "data": {
            "shortcut_name": "Project Master",
            "col": 4
        }
    },
    {
        "type": "shortcut",
        "data": {
            "shortcut_name": "Material Master",
            "col": 4
        }
    }
]''',
        'shortcuts': [
            {
                'label': 'Work Order',
                'link_to': 'Work Order',
                'type': 'DocType',
                'icon': 'file-text',
                'color': 'blue'
            },
            {
                'label': 'MT Inspection', 
                'link_to': 'MT Inspection',
                'type': 'DocType',
                'icon': 'search',
                'color': 'green'
            },
            {
                'label': 'Equipment Master',
                'link_to': 'Equipment Master', 
                'type': 'DocType',
                'icon': 'tool',
                'color': 'orange'
            },
            {
                'label': 'Client Master',
                'link_to': 'Client Master',
                'type': 'DocType', 
                'icon': 'users',
                'color': 'purple'
            },
            {
                'label': 'Branch Master',
                'link_to': 'Branch Master',
                'type': 'DocType',
                'icon': 'map-pin',
                'color': 'red'
            },
            {
                'label': 'Project Master',
                'link_to': 'Project Master',
                'type': 'DocType',
                'icon': 'folder',
                'color': 'yellow'
            },
            {
                'label': 'Material Master',
                'link_to': 'Material Master',
                'type': 'DocType',
                'icon': 'package',
                'color': 'cyan'
            }
        ]
    }
    
    try:
        if frappe.db.exists('Workspace', 'Res Home'):
            workspace = frappe.get_doc('Workspace', 'Res Home')
            workspace.update(workspace_data)
            workspace.save()
            print("   ✓ Updated existing Res Home workspace")
        else:
            workspace = frappe.get_doc(workspace_data)
            workspace.insert()
            print("   ✓ Created new Res Home workspace")
            
    except Exception as e:
        print(f"   ❌ Error setting up workspace: {str(e)}")
        # Don't raise - workspace is nice to have but not critical

def setup_res_roles():
    """Ensure all required roles exist"""
    
    print("👥 Setting up RES roles...")
    
    roles_to_create = [
        {
            'role_name': 'res',
            'desk_access': 1,
            'description': 'Restricted role for NDT isolation layer'
        },
        {
            'role_name': 'NDT Inspector',
            'desk_access': 1, 
            'description': 'NDT Inspector role for alhoty app'
        },
        {
            'role_name': 'NDT Reviewer',
            'desk_access': 1,
            'description': 'NDT Reviewer role for alhoty app'
        }
    ]
    
    for role_data in roles_to_create:
        try:
            if not frappe.db.exists('Role', role_data['role_name']):
                role = frappe.get_doc({
                    'doctype': 'Role',
                    'role_name': role_data['role_name'],
                    'desk_access': role_data['desk_access'],
                    'description': role_data['description']
                })
                role.insert()
                print(f"   ✓ Created role: {role_data['role_name']}")
            else:
                print(f"   ✓ Role already exists: {role_data['role_name']}")
                
        except Exception as e:
            print(f"   ❌ Error creating role {role_data['role_name']}: {str(e)}")

def verify_permissions():
    """Verify that all alhoty doctypes have res role permissions"""
    
    print("🔐 Verifying doctype permissions...")
    
    alhoty_doctypes = [
        'Branch Master', 'Client Master', 'Equipment Master', 
        'Material Master', 'Project Master', 'Work Order', 'MT Inspection'
    ]
    
    for doctype_name in alhoty_doctypes:
        try:
            doctype = frappe.get_doc('DocType', doctype_name)
            has_res_perm = any(p.role == 'res' for p in doctype.permissions)
            
            if has_res_perm:
                print(f"   ✓ {doctype_name} has res permissions")
            else:
                print(f"   ⚠️  {doctype_name} missing res permissions - adding...")
                
                # Add res permissions
                doctype.append('permissions', {
                    'role': 'res',
                    'read': 1,
                    'write': 1,
                    'create': 1,
                    'delete': 1,
                    'submit': 0,
                    'cancel': 0,
                    'amend': 0,
                    'report': 1,
                    'export': 1,
                    'import': 0,
                    'print': 1,
                    'email': 1,
                    'share': 1
                })
                doctype.save()
                print(f"   ✓ Added res permissions to {doctype_name}")
                
        except Exception as e:
            print(f"   ❌ Error checking {doctype_name}: {str(e)}")

def clear_caches():
    """Clear all relevant caches"""
    
    print("🧹 Clearing caches...")
    
    try:
        # Clear NDT whitelist cache
        frappe.cache.delete_value('ndt_res_whitelist')
        
        # Clear session caches
        import redis
        r = frappe.cache
        if hasattr(r, 'delete_keys'):
            r.delete_keys('session:*')
            r.delete_keys('*bootinfo*')
        
        print("   ✓ Caches cleared")
        
    except Exception as e:
        print(f"   ⚠️  Cache clearing failed: {str(e)}")

def execute():
    """Main execution function for bench console"""
    frappe.init()
    frappe.connect()
    frappe.set_user('Administrator')
    
    setup_res_access()
    
    frappe.db.commit()
    print("\n🎉 Setup complete! RES users should now log out and back in.")

if __name__ == '__main__':
    execute()