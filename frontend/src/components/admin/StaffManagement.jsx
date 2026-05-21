import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import './StaffManagement.css';

function StaffManagement() {
  const [staff, setStaff] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [costCenters, setCostCenters] = useState([]);
  const [countries, setCountries] = useState([]);
  const [provinces, setProvinces] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showImportModal, setShowImportModal] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [selectedStaff, setSelectedStaff] = useState(null);
  const [importFile, setImportFile] = useState(null);
  const [importProgress, setImportProgress] = useState(0);

  const [formData, setFormData] = useState({
    employeeid: '',
    fullname: '',
    email: '',
    department: '',
    position: '',
    employmentstatus: 'Active',
    companyid: '',
    costcenterid: '',
    countryid: '',
    provinceid: '',
    departmentid: ''
  });

  const [editFormData, setEditFormData] = useState({
    staffid: '',
    employeeid: '',
    fullname: '',
    email: '',
    department: '',
    position: '',
    employmentstatus: 'Active',
    companyid: '',
    costcenterid: '',
    countryid: '',
    provinceid: '',
    departmentid: ''
  });

  // Cascading derived lists for Create Form
  const filteredProvinces = formData.countryid
    ? provinces.filter(p => p.countryid === parseInt(formData.countryid))
    : [];

  const filteredCompanies = formData.provinceid
    ? companies.filter(c => c.provinceid === parseInt(formData.provinceid))
    : [];

  const filteredDepartments = formData.companyid
    ? departments.filter(d => d.companyid === parseInt(formData.companyid))
    : [];

  const filteredCostCenters = formData.companyid
    ? costCenters.filter(cc => cc.companyid === parseInt(formData.companyid) && cc.isactive !== false)
    : [];



  // Cascading derived lists for Edit Form
  const editFilteredProvinces = editFormData.countryid
    ? provinces.filter(p => p.countryid === parseInt(editFormData.countryid))
    : [];

  const editFilteredCompanies = editFormData.provinceid
    ? companies.filter(c => c.provinceid === parseInt(editFormData.provinceid))
    : [];

  const editFilteredDepartments = editFormData.companyid
    ? departments.filter(d => d.companyid === parseInt(editFormData.companyid))
    : [];

  const editFilteredCostCenters = editFormData.companyid
    ? costCenters.filter(cc => cc.companyid === parseInt(editFormData.companyid) && cc.isactive !== false)
    : [];



  // Cascade handlers for Create Form
  const handleCountryChange = (val) => {
    setFormData(prev => ({
      ...prev,
      countryid: val,
      provinceid: '',
      companyid: '',
      departmentid: '',
      costcenterid: ''
    }));
  };

  const handleProvinceChange = (val) => {
    setFormData(prev => ({
      ...prev,
      provinceid: val,
      companyid: '',
      departmentid: '',
      costcenterid: ''
    }));
  };

  const handleCompanyChange = (val) => {
    setFormData(prev => ({
      ...prev,
      companyid: val,
      departmentid: '',
      costcenterid: ''
    }));
  };

  const handleDepartmentChange = (val) => {
    const deptId = parseInt(val);
    const deptObj = departments.find(d => d.departmentid === deptId);
    const defaultCostCenterId = deptObj && deptObj.costcenterid ? deptObj.costcenterid.toString() : '';
    
    setFormData(prev => ({
      ...prev,
      departmentid: val,
      department: deptObj ? deptObj.departmentname : '',
      costcenterid: defaultCostCenterId || prev.costcenterid
    }));
  };

  // Cascade handlers for Edit Form
  const handleEditCountryChange = (val) => {
    setEditFormData(prev => ({
      ...prev,
      countryid: val,
      provinceid: '',
      companyid: '',
      departmentid: '',
      costcenterid: ''
    }));
  };

  const handleEditProvinceChange = (val) => {
    setEditFormData(prev => ({
      ...prev,
      provinceid: val,
      companyid: '',
      departmentid: '',
      costcenterid: ''
    }));
  };

  const handleEditCompanyChange = (val) => {
    setEditFormData(prev => ({
      ...prev,
      companyid: val,
      departmentid: '',
      costcenterid: ''
    }));
  };

  const handleEditDepartmentChange = (val) => {
    const deptId = parseInt(val);
    const deptObj = departments.find(d => d.departmentid === deptId);
    const defaultCostCenterId = deptObj && deptObj.costcenterid ? deptObj.costcenterid.toString() : '';

    setEditFormData(prev => ({
      ...prev,
      departmentid: val,
      department: deptObj ? deptObj.departmentname : '',
      costcenterid: defaultCostCenterId || prev.costcenterid
    }));
  };

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const staffRes = await api.get('/staff/');
      setStaff(staffRes.data || []);
      
      // Fetch geographic lists
      try {
        const countriesRes = await api.get('/countries/');
        setCountries(countriesRes.data || []);
      } catch (err) {
        console.log('Countries endpoint not available');
      }

      try {
        const provincesRes = await api.get('/provinces/');
        setProvinces(provincesRes.data || []);
      } catch (err) {
        console.log('Provinces endpoint not available');
      }

      try {
        const departmentsRes = await api.get('/departments/');
        setDepartments(departmentsRes.data || []);
      } catch (err) {
        console.log('Departments endpoint not available');
      }

      // Try to fetch companies, locations, and cost centers, but don't fail if they don't exist
      try {
        const companiesRes = await api.get('/companies/');
        setCompanies(companiesRes.data || []);
      } catch (err) {
        console.log('Companies endpoint not available');
      }
      


      try {
        const costCentersRes = await api.get('/cost-centers/');
        setCostCenters(costCentersRes.data || []);
      } catch (err) {
        console.log('Cost Centers endpoint not available');
      }
      
      setError('');
    } catch (err) {
      setError('Failed to load staff');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      employeeid: '',
      fullname: '',
      email: '',
      department: '',
      position: '',
      employmentstatus: 'Active',
      companyid: '',
      costcenterid: '',
      countryid: '',
      provinceid: '',
      departmentid: ''
    });
  };

  const handleCreateStaff = async (e) => {
    e.preventDefault();
    try {
      if (!formData.employeeid || !formData.fullname) {
        setError('Employee ID and Full Name are required');
        return;
      }

      const response = await api.post('/staff/', {
        employeeid: formData.employeeid,
        fullname: formData.fullname,
        email: formData.email,
        department: formData.department,
        position: formData.position,
        employmentstatus: formData.employmentstatus,
        companyid: formData.companyid ? parseInt(formData.companyid) : null,
        locationid: null,
        costcenterid: formData.costcenterid ? parseInt(formData.costcenterid) : null,
        countryid: formData.countryid ? parseInt(formData.countryid) : null,
        provinceid: formData.provinceid ? parseInt(formData.provinceid) : null,
        departmentid: formData.departmentid ? parseInt(formData.departmentid) : null
      });

      setStaff([...staff, response.data]);
      setSuccess('Staff member created successfully!');
      setShowCreateModal(false);
      resetForm();

      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create staff member');
    }
  };

  const handleEditStaff = async (e) => {
    e.preventDefault();
    try {
      if (!editFormData.fullname) {
        setError('Full Name is required');
        return;
      }

      const response = await api.put(`/staff/${editFormData.staffid}`, {
        fullname: editFormData.fullname,
        email: editFormData.email,
        department: editFormData.department,
        position: editFormData.position,
        employmentstatus: editFormData.employmentstatus,
        companyid: editFormData.companyid ? parseInt(editFormData.companyid) : null,
        locationid: null,
        costcenterid: editFormData.costcenterid ? parseInt(editFormData.costcenterid) : null,
        countryid: editFormData.countryid ? parseInt(editFormData.countryid) : null,
        provinceid: editFormData.provinceid ? parseInt(editFormData.provinceid) : null,
        departmentid: editFormData.departmentid ? parseInt(editFormData.departmentid) : null
      });

      setStaff(staff.map(s => s.staffid === editFormData.staffid ? response.data : s));
      setSuccess('Staff member updated successfully!');
      setShowEditModal(false);
      setEditFormData({
        staffid: '',
        employeeid: '',
        fullname: '',
        email: '',
        department: '',
        position: '',
        employmentstatus: 'Active',
        companyid: '',
        costcenterid: '',
        countryid: '',
        provinceid: '',
        departmentid: ''
      });

      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update staff member');
    }
  };

  const handleDeleteStaff = async () => {
    try {
      await api.delete(`/staff/${selectedStaff.staffid}`);
      setStaff(staff.filter(s => s.staffid !== selectedStaff.staffid));
      setSuccess('Staff member deleted successfully!');
      setShowDeleteConfirm(false);
      setSelectedStaff(null);
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to delete staff member');
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (!file.name.match(/\.(xlsx|xls|csv)$/)) {
        setError('Please select a valid Excel file (.xlsx, .xls, or .csv)');
        return;
      }
      setImportFile(file);
      setError('');
    }
  };

  const handleImportStaff = async (e) => {
    e.preventDefault();
    if (!importFile) {
      setError('Please select a file to import');
      return;
    }

    try {
      setLoading(true);
      const formDataToSend = new FormData();
      formDataToSend.append('file', importFile);

      const response = await api.post('/staff/import', formDataToSend, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          setImportProgress(percentCompleted);
        }
      });

      setStaff(response.data.staff || []);
      setSuccess(`Successfully imported ${response.data.imported_count || 0} staff members!`);
      setShowImportModal(false);
      setImportFile(null);
      setImportProgress(0);

      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to import staff members');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const downloadTemplate = () => {
    const template = `Employee ID,Full Name,Email,Department,Position,Company,Employment Status
EMP001,John Doe,john@example.com,IT,Developer,Acme Corp,Active
EMP002,Jane Smith,jane@example.com,HR,Manager,Acme Corp,Active
EMP003,Bob Johnson,bob@example.com,Finance,Analyst,Tech Solutions,Active`;

    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(template));
    element.setAttribute('download', 'staff_template.csv');
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  if (loading && staff.length === 0) {
    return <div className="loading">Loading staff...</div>;
  }

  return (
    <div className="staff-management-container">
      <div className="staff-header">
        <h3>👥 Staff Management</h3>
        <div className="staff-actions">
          <button
            className="btn btn-primary"
            onClick={() => {
              resetForm();
              setShowCreateModal(true);
            }}
          >
            ➕ Add Staff Member
          </button>
          <button
            className="btn btn-success"
            onClick={() => setShowImportModal(true)}
          >
            📥 Import from Excel
          </button>
        </div>
      </div>

      {error && (
        <div className="alert alert-error">
          {error}
          <button onClick={() => setError('')} className="close-alert">✕</button>
        </div>
      )}
      {success && (
        <div className="alert alert-success">
          {success}
          <button onClick={() => setSuccess('')} className="close-alert">✕</button>
        </div>
      )}

      <div className="staff-table-container">
        {staff.length === 0 ? (
          <div className="empty-state">
            <p>No staff members found</p>
            <button
              className="btn btn-primary"
              onClick={() => {
                resetForm();
                setShowCreateModal(true);
              }}
            >
              Add First Staff Member
            </button>
          </div>
        ) : (
          <table className="staff-table">
            <thead>
              <tr>
                <th>Employee ID</th>
                <th>Full Name</th>
                <th>Email</th>
                <th>Country</th>
                <th>Province</th>
                <th>Company</th>
                <th>Department</th>
                <th>Position</th>
                <th>Cost Center</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {staff.map(member => {
                const country = countries.find(c => c.countryid === member.countryid);
                const province = provinces.find(p => p.provinceid === member.provinceid);
                const company = companies.find(c => c.companyid === member.companyid);
                const costcenter = costCenters.find(cc => cc.costcenterid === member.costcenterid);
                const departmentName = member.departmentid 
                  ? (departments.find(d => d.departmentid === member.departmentid)?.departmentname || member.department)
                  : member.department;
                
                return (
                  <tr key={member.staffid}>
                    <td>
                      <code>{member.employeeid}</code>
                    </td>
                    <td>{member.fullname}</td>
                    <td>{member.email || '-'}</td>
                    <td>{country ? country.countryname : '-'}</td>
                    <td>{province ? province.provincename : '-'}</td>
                    <td>{company ? company.companyname : '-'}</td>
                    <td>{departmentName || '-'}</td>
                    <td>{member.position || '-'}</td>
                    <td>
                      {costcenter ? (
                        <span className="cc-badge" title={costcenter.costcentername}>
                          {costcenter.costcentercode}
                        </span>
                      ) : (
                        '-'
                      )}
                    </td>
                    <td>
                      <span className={`status-badge status-${member.employmentstatus?.toLowerCase()}`}>
                        {member.employmentstatus || 'Active'}
                      </span>
                    </td>
                    <td>
                      <button
                        className="btn btn-sm btn-primary"
                        onClick={() => {
                          setEditFormData({
                            staffid: member.staffid,
                            employeeid: member.employeeid,
                            fullname: member.fullname,
                            email: member.email || '',
                            department: member.department || '',
                            position: member.position || '',
                            employmentstatus: member.employmentstatus || 'Active',
                            companyid: member.companyid || '',
                            costcenterid: member.costcenterid || '',
                            countryid: member.countryid || '',
                            provinceid: member.provinceid || '',
                            departmentid: member.departmentid || ''
                          });
                          setShowEditModal(true);
                        }}
                        title="Edit Staff"
                      >
                        ✏️ Edit
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>

      {/* Create Staff Modal */}
      {showCreateModal && (
        <div className="modal-overlay" onClick={() => setShowCreateModal(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h2>➕ Add Staff Member</h2>
              <button
                className="close-btn"
                onClick={() => setShowCreateModal(false)}
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleCreateStaff}>
              <div className="form-group">
                <label>Employee ID *</label>
                <input
                  type="text"
                  name="employeeid"
                  value={formData.employeeid}
                  onChange={handleInputChange}
                  placeholder="e.g., EMP001"
                  className="form-control"
                  required
                />
              </div>

              <div className="form-group">
                <label>Full Name *</label>
                <input
                  type="text"
                  name="fullname"
                  value={formData.fullname}
                  onChange={handleInputChange}
                  placeholder="John Doe"
                  className="form-control"
                  required
                />
              </div>

              <div className="form-group">
                <label>Email</label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  placeholder="john@example.com"
                  className="form-control"
                />
              </div>

              <div className="form-group">
                <label>Position</label>
                <input
                  type="text"
                  name="position"
                  value={formData.position}
                  onChange={handleInputChange}
                  placeholder="Developer, Manager, etc."
                  className="form-control"
                />
              </div>

              <div className="form-group">
                <label>Employment Status</label>
                <select
                  name="employmentstatus"
                  value={formData.employmentstatus}
                  onChange={handleInputChange}
                  className="form-control"
                >
                  <option value="Active">Active</option>
                  <option value="Inactive">Inactive</option>
                  <option value="On Leave">On Leave</option>
                  <option value="Terminated">Terminated</option>
                </select>
              </div>

              {/* Geographic and Corporate Organization Cascade Banner */}
              <div style={{
                display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                background: 'linear-gradient(90deg, rgba(99,102,241,0.08), rgba(139,92,246,0.08))',
                border: '1px solid rgba(99,102,241,0.15)', borderRadius: '8px',
                padding: '10px 16px', marginTop: '16px', marginBottom: '16px',
                fontSize: '13px', fontWeight: 600, color: '#6366f1',
              }}>
                <span>🌍 Organization Mapping</span>
                <span style={{ fontSize: '11px', color: '#818cf8', fontWeight: 400 }}>
                  Country → Province → Company → Department → Cost Center
                </span>
              </div>

              {/* Country */}
              <div className="form-group">
                <label>Country *</label>
                <select
                  name="countryid"
                  value={formData.countryid}
                  onChange={(e) => handleCountryChange(e.target.value)}
                  className="form-control"
                  required
                >
                  <option value="">-- Select Country --</option>
                  {countries.map(c => (
                    <option key={c.countryid} value={c.countryid}>
                      {c.countryname} ({c.countrycode})
                    </option>
                  ))}
                </select>
              </div>

              {/* Province */}
              <div className="form-group">
                <label>Province *</label>
                <select
                  name="provinceid"
                  value={formData.provinceid}
                  onChange={(e) => handleProvinceChange(e.target.value)}
                  disabled={!formData.countryid}
                  className="form-control"
                  required
                >
                  <option value="">
                    {!formData.countryid ? '-- Select Country First --' : '-- Select Province --'}
                  </option>
                  {filteredProvinces.map(p => (
                    <option key={p.provinceid} value={p.provinceid}>
                      {p.provincename} ({p.provincecode})
                    </option>
                  ))}
                </select>
              </div>

              {/* Company */}
              <div className="form-group">
                <label>Company *</label>
                <select
                  name="companyid"
                  value={formData.companyid}
                  onChange={(e) => handleCompanyChange(e.target.value)}
                  disabled={!formData.provinceid}
                  className="form-control"
                  required
                >
                  <option value="">
                    {!formData.provinceid ? '-- Select Province First --' : '-- Select Company --'}
                  </option>
                  {filteredCompanies.map(c => (
                    <option key={c.companyid} value={c.companyid}>
                      {c.companyname} ({c.companycode})
                    </option>
                  ))}
                </select>
              </div>

              {/* Department */}
              <div className="form-group">
                <label>Department *</label>
                <select
                  name="departmentid"
                  value={formData.departmentid}
                  onChange={(e) => handleDepartmentChange(e.target.value)}
                  disabled={!formData.companyid}
                  className="form-control"
                  required
                >
                  <option value="">
                    {!formData.companyid ? '-- Select Company First --' : '-- Select Department --'}
                  </option>
                  {filteredDepartments.map(d => (
                    <option key={d.departmentid} value={d.departmentid}>
                      {d.departmentname} ({d.departmentcode})
                    </option>
                  ))}
                </select>
              </div>

              {/* Cost Center */}
              <div className="form-group">
                <label>Cost Center</label>
                <select
                  name="costcenterid"
                  value={formData.costcenterid}
                  onChange={(e) => setFormData(prev => ({ ...prev, costcenterid: e.target.value }))}
                  className="form-control"
                  disabled={!formData.companyid}
                >
                  <option value="">
                    {!formData.companyid
                      ? '-- Select Company First --'
                      : filteredCostCenters.length === 0
                        ? '-- No Cost Centers for this Company --'
                        : '-- Select Cost Center --'}
                  </option>
                  {filteredCostCenters.map(cc => (
                    <option key={cc.costcenterid} value={cc.costcenterid}>
                      {cc.costcentername} ({cc.costcentercode})
                    </option>
                  ))}
                </select>
              </div>



              <div className="modal-actions">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setShowCreateModal(false)}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn btn-primary"
                >
                  Add Staff Member
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edit Staff Modal */}
      {showEditModal && (
        <div className="modal-overlay" onClick={() => setShowEditModal(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h2>✏️ Edit Staff Member</h2>
              <button
                className="close-btn"
                onClick={() => setShowEditModal(false)}
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleEditStaff}>
              <div className="form-group">
                <label>Employee ID</label>
                <input
                  type="text"
                  value={editFormData.employeeid}
                  className="form-control"
                  disabled
                />
                <small>Employee ID cannot be changed</small>
              </div>

              <div className="form-group">
                <label>Full Name *</label>
                <input
                  type="text"
                  name="fullname"
                  value={editFormData.fullname}
                  onChange={(e) => setEditFormData({...editFormData, fullname: e.target.value})}
                  placeholder="John Doe"
                  className="form-control"
                  required
                />
              </div>

              <div className="form-group">
                <label>Email</label>
                <input
                  type="email"
                  name="email"
                  value={editFormData.email}
                  onChange={(e) => setEditFormData({...editFormData, email: e.target.value})}
                  placeholder="john@example.com"
                  className="form-control"
                />
              </div>

              <div className="form-group">
                <label>Position</label>
                <input
                  type="text"
                  name="position"
                  value={editFormData.position}
                  onChange={(e) => setEditFormData({...editFormData, position: e.target.value})}
                  placeholder="Developer, Manager, etc."
                  className="form-control"
                />
              </div>

              <div className="form-group">
                <label>Employment Status</label>
                <select
                  name="employmentstatus"
                  value={editFormData.employmentstatus}
                  onChange={(e) => setEditFormData({...editFormData, employmentstatus: e.target.value})}
                  className="form-control"
                >
                  <option value="Active">Active</option>
                  <option value="Inactive">Inactive</option>
                  <option value="On Leave">On Leave</option>
                  <option value="Terminated">Terminated</option>
                </select>
              </div>

              {/* Geographic and Corporate Organization Cascade Banner */}
              <div style={{
                display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                background: 'linear-gradient(90deg, rgba(99,102,241,0.08), rgba(139,92,246,0.08))',
                border: '1px solid rgba(99,102,241,0.15)', borderRadius: '8px',
                padding: '10px 16px', marginTop: '16px', marginBottom: '16px',
                fontSize: '13px', fontWeight: 600, color: '#6366f1',
              }}>
                <span>🌍 Organization Mapping</span>
                <span style={{ fontSize: '11px', color: '#818cf8', fontWeight: 400 }}>
                  Country → Province → Company → Department → Cost Center
                </span>
              </div>

              {/* Country */}
              <div className="form-group">
                <label>Country *</label>
                <select
                  name="countryid"
                  value={editFormData.countryid}
                  onChange={(e) => handleEditCountryChange(e.target.value)}
                  className="form-control"
                  required
                >
                  <option value="">-- Select Country --</option>
                  {countries.map(c => (
                    <option key={c.countryid} value={c.countryid}>
                      {c.countryname} ({c.countrycode})
                    </option>
                  ))}
                </select>
              </div>

              {/* Province */}
              <div className="form-group">
                <label>Province *</label>
                <select
                  name="provinceid"
                  value={editFormData.provinceid}
                  onChange={(e) => handleEditProvinceChange(e.target.value)}
                  disabled={!editFormData.countryid}
                  className="form-control"
                  required
                >
                  <option value="">
                    {!editFormData.countryid ? '-- Select Country First --' : '-- Select Province --'}
                  </option>
                  {editFilteredProvinces.map(p => (
                    <option key={p.provinceid} value={p.provinceid}>
                      {p.provincename} ({p.provincecode})
                    </option>
                  ))}
                </select>
              </div>

              {/* Company */}
              <div className="form-group">
                <label>Company *</label>
                <select
                  name="companyid"
                  value={editFormData.companyid}
                  onChange={(e) => handleEditCompanyChange(e.target.value)}
                  disabled={!editFormData.provinceid}
                  className="form-control"
                  required
                >
                  <option value="">
                    {!editFormData.provinceid ? '-- Select Province First --' : '-- Select Company --'}
                  </option>
                  {editFilteredCompanies.map(c => (
                    <option key={c.companyid} value={c.companyid}>
                      {c.companyname} ({c.companycode})
                    </option>
                  ))}
                </select>
              </div>

              {/* Department */}
              <div className="form-group">
                <label>Department *</label>
                <select
                  name="departmentid"
                  value={editFormData.departmentid}
                  onChange={(e) => handleEditDepartmentChange(e.target.value)}
                  disabled={!editFormData.companyid}
                  className="form-control"
                  required
                >
                  <option value="">
                    {!editFormData.companyid ? '-- Select Company First --' : '-- Select Department --'}
                  </option>
                  {editFilteredDepartments.map(d => (
                    <option key={d.departmentid} value={d.departmentid}>
                      {d.departmentname} ({d.departmentcode})
                    </option>
                  ))}
                </select>
              </div>

              {/* Cost Center */}
              <div className="form-group">
                <label>Cost Center</label>
                <select
                  name="costcenterid"
                  value={editFormData.costcenterid}
                  onChange={(e) => setEditFormData(prev => ({ ...prev, costcenterid: e.target.value }))}
                  className="form-control"
                  disabled={!editFormData.companyid}
                >
                  <option value="">
                    {!editFormData.companyid
                      ? '-- Select Company First --'
                      : editFilteredCostCenters.length === 0
                        ? '-- No Cost Centers for this Company --'
                        : '-- Select Cost Center --'}
                  </option>
                  {editFilteredCostCenters.map(cc => (
                    <option key={cc.costcenterid} value={cc.costcenterid}>
                      {cc.costcentername} ({cc.costcentercode})
                    </option>
                  ))}
                </select>
              </div>



              <div className="modal-actions">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setShowEditModal(false)}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn btn-primary"
                >
                  Update Staff Member
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Import Staff Modal */}
      {showImportModal && (
        <div className="modal-overlay" onClick={() => setShowImportModal(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h2>📥 Import Staff from Excel</h2>
              <button
                className="close-btn"
                onClick={() => setShowImportModal(false)}
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleImportStaff}>
              <div className="import-info">
                <h4>📋 Import Instructions</h4>
                <ul>
                  <li>Download the template file below</li>
                  <li>Fill in your staff data in the Excel file</li>
                  <li>Required columns: Employee ID, Full Name</li>
                  <li>Optional columns: Email, Department, Position, Company, Employment Status</li>
                  <li>Company must match existing records in the system</li>
                  <li>Upload the completed file</li>
                </ul>
              </div>

              <div className="template-section">
                <button
                  type="button"
                  className="btn btn-outline"
                  onClick={downloadTemplate}
                >
                  📥 Download Template
                </button>
              </div>

              <div className="form-group">
                <label>Select Excel File *</label>
                <div className="file-input-wrapper">
                  <input
                    type="file"
                    accept=".xlsx,.xls,.csv"
                    onChange={handleFileChange}
                    className="file-input"
                    required
                  />
                  <span className="file-input-label">
                    {importFile ? importFile.name : 'Choose file...'}
                  </span>
                </div>
                <small>Supported formats: .xlsx, .xls, .csv</small>
              </div>

              {importProgress > 0 && importProgress < 100 && (
                <div className="progress-bar">
                  <div className="progress-fill" style={{ width: `${importProgress}%` }}>
                    {importProgress}%
                  </div>
                </div>
              )}

              <div className="modal-actions">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => {
                    setShowImportModal(false);
                    setImportFile(null);
                    setImportProgress(0);
                  }}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn btn-success"
                  disabled={loading || !importFile}
                >
                  {loading ? 'Importing...' : 'Import Staff'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && selectedStaff && (
        <div className="modal-overlay" onClick={() => setShowDeleteConfirm(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h2>🗑️ Delete Staff Member</h2>
            </div>

            <div className="modal-body">
              <p>Are you sure you want to delete this staff member?</p>
              <p className="staff-info">
                <strong>{selectedStaff.fullname}</strong><br />
                {selectedStaff.employeeid}
              </p>
              <p className="warning">This action cannot be undone.</p>
            </div>

            <div className="modal-actions">
              <button
                className="btn btn-secondary"
                onClick={() => setShowDeleteConfirm(false)}
              >
                Cancel
              </button>
              <button
                className="btn btn-danger"
                onClick={handleDeleteStaff}
              >
                Delete Staff Member
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default StaffManagement;
