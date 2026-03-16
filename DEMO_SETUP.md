# AL HOTY NDT Demo - Complete Setup Guide

## Overview
This demo implements a complete MT UV Fluorescent inspection workflow from Work Order to PDF with electronic signature capability.

## ✅ SYSTEM STATUS: READY FOR DEMO

### 8 Doctypes Created & Working
1. **Branch Master** - 5 branches (Riyadh, Dammam, Jeddah, Jubail, Yanbu)
2. **Client Master** - 3 clients (Saudi Aramco, SABIC, SEC)
3. **Project Master** - 3 projects linked to clients
4. **Equipment Master** - 7 equipment records with serial number lookup
5. **Material Master** - Material registry with quick-add capability
6. **Work Order** - 5 demo work orders across branches
7. **MT Inspection** - 3 demo inspections with complete data
8. **MT Inspection Result** - Child table for inspection results

### ✅ Key Features Working
- ✅ Equipment serial number → manufacturer auto-fill
- ✅ Work Order → Client/Project auto-fetch on MT Inspection
- ✅ Electronic signature with one-click inclusion
- ✅ Branch hierarchy (everything starts from branch level)
- ✅ Select fields with empty first options (no pre-selection)
- ✅ Equipment serial numbers as Link fields with dropdowns
- ✅ 2 test users (Inspector + Reviewer) with strong passwords
- ✅ Dashboard workspace with KPI cards and charts
- ✅ Demo data loaded and ready

### 🎯 Dashboard Features
- **4 KPI Cards**: Active Work Orders, Pending Inspections, Equipment Due Calibration, Total Branches
- **4 Charts**: Work Orders by Status, Equipment by Branch, Equipment by Type, Monthly Inspection Trend
- **7 Shortcuts**: Quick access to all main doctypes
- **2 Quick Lists**: Recent Work Orders and MT Inspections
- **Professional Layout**: Impressive landing page for client demo

## Installation Steps

### Step 1: Setup Complete ✅
All setup scripts have been run successfully:
- Roles: NDT Inspector, NDT Reviewer
- Users: inspector@alhoty.com, reviewer@alhoty.com
- Custom Field: User.signature_image
- Master Data: 5 branches, 3 clients, 3 projects, 7 equipment
- Demo Data: 5 work orders, 3 MT inspections
- Naming Series: WO-.YYYY.-.#### and MTI-.YYYY.-.####

### Step 2: Upload Signature (Important!)
1. Login as `inspector@alhoty.com` (password: `Inspector@2024!`)
2. Click your profile icon → My Settings
3. Scroll to "Signature" field
4. Upload a signature image (PNG/JPG)
5. Save

### Step 3: Access Dashboard
1. Login to system
2. Go to "AL HOTY Dashboard" workspace
3. See live KPI cards and charts
4. Use shortcuts for quick navigation

## Demo Workflow - Ready to Test

#### 1. Dashboard Overview
- Access "AL HOTY Dashboard" workspace
- View KPI cards showing live data
- Charts display work orders and equipment distribution
- Quick access to all modules via shortcuts

#### 2. Create Work Order
1. Go to Work Order list (or use dashboard shortcut)
2. Click New
3. Fill in:
   - Branch: Select from dropdown (Dammam, Riyadh, etc.)
   - Client: Select from dropdown (Saudi Aramco, SABIC, SEC)
   - Project Name: Auto-filtered based on client
   - Location: Auto-filled from Project
   - Work Order Date: Today
4. Save → Auto-generates WO-2026-0001 format

#### 3. Create MT Inspection
1. From saved Work Order, click "+ New MT Inspection" button
2. Notice: Work Order, Branch, Client, Project, Location are auto-filled
3. Fill Examination Technique section:
   - MT Variant: Select "MT UV Fluorescent" (no pre-selection)
   - Magnetizing Technique: Select from dropdown
   - All other fields start empty
4. Fill Equipment section (Link fields with dropdowns):
   - Yoke Serial No: Select `27418` → PARKER auto-fills
   - UV Light Serial No: Select `1947904` → SPECTROLINE auto-fills
   - Light Meter Serial No: Select `1098116` → SPECTRONICS CORP auto-fills
   - Gauss Meter Serial No: Select `2379` → R.BANNIS Co auto-fills
   - Thermometer Serial No: Select `20120700` → SMART SENSOR auto-fills
5. Fill remaining sections
6. Check "Include Electronic Signature" → signature preview appears
7. Save → Auto-generates MTI-2026-0001 format

#### 4. Generate PDF & Workflow
1. Click Print → MT Inspection Report
2. PDF shows all data + signature block
3. Use workflow actions for approval process

## Demo Data Available

### Branches (5)
- Riyadh Branch (RYD)
- Dammam Branch (DMM) 
- Jeddah Branch (JED)
- Jubail Branch (JUB)
- Yanbu Branch (YNB)

### Equipment (7 records)
| Serial No | Manufacturer | Type | Branch |
|-----------|--------------|------|---------|
| 27418 | PARKER | Yoke | Dammam |
| 1947904 | SPECTROLINE | UV Light | Dammam |
| 1098116 | SPECTRONICS CORP | Light Meter | Dammam |
| 2379 | R.BANNIS Co | Gauss Meter | Dammam |
| 20120700 | SMART SENSOR | Thermometer | Dammam |
| RYD-001 | PARKER | Yoke | Riyadh |
| JED-001 | MAGNAFLUX | Yoke | Jeddah |

### Work Orders (5 demo records)
- WO-2026-00002: Dammam Branch - Saudi Aramco (Open)
- WO-2026-00003: Riyadh Branch - SABIC (Open)  
- WO-2026-00004: Jeddah Branch - SEC (Completed)
- WO-2026-00005: Jubail Branch - Saudi Aramco (In Progress)
- WO-2026-00006: Yanbu Branch - SABIC (Completed)

### MT Inspections (3 demo records)
- MTI-2026-0001: From WO-2026-00006 (Yanbu Branch)
- MTI-2026-0002: From WO-2026-00005 (Jubail Branch)
- MTI-2026-0003: From WO-2026-00004 (Jeddah Branch)

## Test Users

| Email | Password | Role |
|-------|----------|------|
| inspector@alhoty.com | Inspector@2024! | NDT Inspector |
| reviewer@alhoty.com | Reviewer@2024! | NDT Reviewer |

## System URLs
- **Main Site**: http://alhoty.local:8000
- **Dashboard**: http://alhoty.local:8000/app/al-hoty-dashboard
- **Work Orders**: http://alhoty.local:8000/app/work-order
- **MT Inspections**: http://alhoty.local:8000/app/mt-inspection

## Client Demo Script

### 1. Dashboard Showcase (2 minutes)
- "Welcome to AL HOTY NDT Operations Center"
- Show live KPI cards with real data
- Demonstrate charts showing work distribution
- Highlight professional interface design

### 2. Master Data Hierarchy (2 minutes)
- Show Branch Master → Equipment relationship
- Demonstrate Client → Project linkage
- Explain how everything starts from branch level

### 3. Work Order Creation (3 minutes)
- Create new work order
- Show branch selection and auto-population
- Demonstrate client/project integration

### 4. MT Inspection Workflow (5 minutes)
- Create inspection from work order
- Show equipment serial number dropdowns
- Demonstrate manufacturer auto-fill
- Show empty select field options (no pre-selection)
- Upload signature and enable electronic signing
- Generate PDF report

### 5. Dashboard Analytics (2 minutes)
- Return to dashboard
- Show updated KPI cards
- Demonstrate real-time data updates

## Technical Notes

### Customization Ready
- Print format can be customized with client's template
- Workflow states can be modified
- Additional fields can be added easily
- Charts and KPIs can be customized

### Production Deployment
- Export fixtures for production import
- Configure proper domain and SSL
- Set up backup procedures
- Configure email notifications

## Support & Next Steps

✅ **System is demo-ready**
✅ **All features working as specified**  
✅ **Dashboard impressive and functional**
✅ **Complete workflow tested**

The AL HOTY NDT Demo System is now complete and ready for client presentation. All requested features are implemented and working correctly.
