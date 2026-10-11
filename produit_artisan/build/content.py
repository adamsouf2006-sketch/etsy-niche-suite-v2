BRAND="Oakfold"; KIT="Handyman & Contractor Kit"; ACC="#D9480F"; ACC2="#1F2933"; SOFT="#FDEBDD"
DOCS=[
("01","Independent Contractor Agreement","Client - contractor terms",[
 ("h","Parties"),("f",[("Contractor / business name",2),("License # (if any)",1)]),("f",[("Contractor address",2),("Phone",1)]),("f",[("Client name",2),("Phone",1)]),("f",[("Project address",2),("Email",1)]),
 ("h","Project"),("f",[("Description of work",3)]),("f",[("Start date",1),("Estimated completion",1),("Estimate # attached",1)]),
 ("f",[("Total price ($)",1),("Deposit ($)",1),("Balance due",1)]),("c",4,["Cash","Check","Card","Bank transfer"]),
 ("h","Terms"),("clauses",["Scope. The contractor performs the work described above and in the attached estimate. Any change is agreed in writing on a Change Order before it is done.",
 "Independent contractor. The contractor works independently, supplies tools and controls how the work is done. Nothing here creates an employment relationship.",
 "Materials. Materials are included unless listed otherwise. Client-supplied materials are the client's responsibility.",
 "Payment. The deposit is due on signing; the balance is due on completion. Late payments may carry the fee shown below.",
 "Site access. The client provides access, utilities and a clear work area during agreed hours.",
 "Delays. The contractor is not responsible for delays caused by weather, material shortages or hidden conditions; the client is informed promptly.",
 "Warranty. Workmanship is guaranteed for the period shown below. Manufacturer warranties apply to materials.",
 "Insurance and permits. The contractor carries general liability insurance. Permits are obtained by the party shown below.",
 "Cancellation. Either party may cancel in writing; work completed and materials ordered up to that date are paid."]),
 ("f",[("Late fee",1),("Workmanship warranty",1),("Permits obtained by",1)]),("sig",["Contractor","Client"]),
 ("note","General template, not legal advice. Contractor rules differ by state and country; have it reviewed locally.")]),
("02","Job Estimate","Valid for 30 days",[
 ("f",[("Estimate #",1),("Date",1),("Valid until",1)]),("f",[("Client",2),("Phone",1)]),("f",[("Job address",2),("Email",1)]),
 ("h","Labor"),("t",["Task","Hours","Rate ($)","Amount ($)"],7),
 ("h","Materials"),("t",["Item","Qty","Unit cost ($)","Amount ($)"],7),
 ("f",[("Labor total ($)",1),("Materials total ($)",1),("Tax ($)",1)]),("f",[("ESTIMATE TOTAL ($)",1),("Deposit required ($)",1),("Est. duration",1)]),
 ("f",[("Notes and exclusions",3)]),("sig",["Accepted by client"])]),
("03","Work Order","Job details for the crew",[
 ("f",[("Work order #",1),("Date",1),("Priority",1)]),("f",[("Client",2),("Phone",1)]),("f",[("Job address",2),("Gate / access code",1)]),
 ("c",4,["Repair","Installation","Maintenance","Inspection","Assembly","Painting","Plumbing","Electrical"]),
 ("f",[("Work requested",3)]),("f",[("Assigned to",1),("Scheduled date",1),("Time window",1)]),
 ("h","Time & materials"),("t",["Date","Worker","Time in","Time out","Hours"],4),("t",["Material / part","Qty","Cost ($)"],5),
 ("f",[("Work performed / notes",3)]),("c",3,["Job complete","Follow-up needed","Parts on order"]),("sig",["Technician","Client"])]),
("04","Change Order","Changes to the original agreement",[
 ("f",[("Change order #",1),("Date",1),("Original estimate #",1)]),("f",[("Client",2),("Phone",1)]),("f",[("Project address",3)]),
 ("h","Change requested"),("f",[("Description of the change",3)]),("f",[("Reason (client request, hidden damage, code...)",3)]),
 ("h","Cost & schedule impact"),("t",["Item","Labor ($)","Materials ($)","Total ($)"],5),
 ("f",[("Original contract ($)",1),("This change ($)",1),("New contract total ($)",1)]),("f",[("Schedule change (days)",1),("New completion date",1),("Payment due",1)]),
 ("c",2,["Approved - proceed with the change","Declined - continue original scope"]),("sig",["Contractor","Client"])]),
("05","Material List","Plan and track job supplies",[
 ("f",[("Project",2),("Date",1)]),("f",[("Client",2),("Supplier",1)]),
 ("t",["Item / description","Size / spec","Qty","Unit cost ($)","Total ($)","Bought"],20),
 ("f",[("Materials subtotal ($)",1),("Tax ($)",1),("Total ($)",1)]),("f",[("Notes",3)])]),
("06","Job Completion & Sign-Off","Final walkthrough",[
 ("f",[("Client",2),("Job #",1)]),("f",[("Project address",2),("Completion date",1)]),("f",[("Work completed",3)]),
 ("h","Walkthrough checklist"),("c",2,["All work done as agreed","Area cleaned, debris removed","Fixtures and finishes checked","Client shown how to use / care","Warranty information given","Photos taken (before / after)"]),
 ("t",["Punch list item","Who","Due date","Done"],6),
 ("f",[("Final amount ($)",1),("Paid to date ($)",1),("Balance ($)",1)]),
 ("c",1,["I confirm the work is complete and satisfactory, except any punch list items above."]),("sig",["Client","Contractor"])]),
("07","Invoice","Thank you for your business",[
 ("f",[("Invoice #",1),("Date",1),("Due date",1)]),("f",[("Bill to",2),("Phone",1)]),("f",[("Job address",2),("Email",1)]),
 ("t",["Date","Description","Qty / hrs","Rate ($)","Amount ($)"],12),
 ("f",[("Subtotal ($)",1),("Tax ($)",1),("Deposit paid ($)",1)]),("f",[("TOTAL DUE ($)",1),("Payment terms",1),("Late fee",1)]),
 ("c",4,["Cash","Check","Card","Bank transfer"]),("f",[("Payment details / notes",3)])]),
("08","Client Intake & Job Request","First call / site visit",[
 ("f",[("Client name",2),("Date",1)]),("f",[("Phone",1),("Email",1),("Preferred contact",1)]),("f",[("Job address",2),("Property type",1)]),("f",[("How did you hear about us?",2),("Referral by",1)]),
 ("h","Job request"),("c",4,["Repair","Remodel","Installation","Maintenance"]),("f",[("Describe the job",3)]),("t",["Room / area","Problem / request","Photos taken"],5),
 ("h","Budget & timing"),("f",[("Budget range ($)",1),("Desired start",1),("Deadline",1)]),("c",3,["Owner","Tenant (landlord approval needed)","Property manager"]),
 ("f",[("Site visit date / time",1),("Estimate due by",1),("Pets / access notes",1)]),("f",[("Notes",3)])]),
]
