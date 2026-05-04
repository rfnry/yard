# Conflict Checks

A conflict screen happens **before** a `case_id` is opened, not
during. By the time a turn arrives under a `case_id`, the firm has
already cleared the conflict.

Two situations during a turn can resurface a conflict:

1. A `BusinessRegistry` lookup reveals the subject is a principal of
   an entity adverse to a current firm client.
2. An `EmploymentHistory` lookup reveals the subject has worked at
   a firm-client business in the last 5 years.

Either one is a `Followups` flag, not a refusal to continue. The
attorney decides whether to proceed; the assistant just makes sure
the conflict is visible in the report rather than left for the
attorney to spot in the raw data.
