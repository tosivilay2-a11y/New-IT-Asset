# Quick Reference: Status & Location Updates

## Check-Out
```
Status: In Use (statusid = 2)
Condition: Good
Location: Unchanged
Assigned To: Staff member
```

## Check-In (Based on Condition)

### Good Condition
```
Status: Available (statusid = 1)
Condition: Good
Location: Staff's location
Assigned To: Unassigned
```

### Fair Condition
```
Status: Available (statusid = 1)
Condition: Fair
Location: Staff's location
Assigned To: Unassigned
```

### Damaged Condition
```
Status: Maintenance (statusid = 3)
Condition: Damaged
Location: Staff's location
Assigned To: Unassigned
```

### Broken Condition
```
Status: Retired (statusid = 4)
Condition: Broken
Location: Staff's location
Assigned To: Unassigned
```

## Status IDs
- 1 = Available
- 2 = In Use
- 3 = Maintenance
- 4 = Retired/Disposed

## Location
- Check-Out: Unchanged
- Check-In: Set to staff member's assigned location

