# OMP + Matt Pocock Skills + Herdr + AGY Workflow

## 1. Mục tiêu

Workflow này phân chia trách nhiệm rõ ràng giữa các thành phần:

- **User**: quyết định yêu cầu sản phẩm và phê duyệt spec/tickets.
- **OMP**: discovery, planning, architecture, specification và orchestration.
- **Matt Pocock Skills**: development lifecycle và engineering discipline.
- **Herdr**: quản lý terminal panes và agent lifecycle.
- **AGY + Gemini**: implementation worker.
- **AGY Verifier**: independent code review và qualitative verification.
- **Git**: lưu các implementation checkpoint đã được chấp nhận.
- **GitHub/GitLab Issues hoặc local tickets**: lưu ticket graph và dependency state.

Nguyên tắc chính:

> OMP là brain và conductor.
> AGY là implementation worker.
> Một ticket tương ứng với một fresh AGY implementation context.

---

# 2. High-level Workflow

```text
User
 │
 ▼
OMP
 │
 ├─ grill-with-docs
 │
 ├─ to-spec
 │
 └─ to-tickets
 │
 ▼
User approves tickets
 │
 ▼
ship-with-agy
 │
 ▼
OMP Conductor
 │
 ├─ compute ticket frontier
 ├─ select one unblocked ticket
 ├─ start fresh AGY implementer
 ├─ collect implementation
 ├─ freeze candidate
 ├─ run deterministic verification
 ├─ start fresh AGY verifier
 ├─ evaluate evidence
 ├─ remediate if needed
 ├─ commit accepted ticket
 ├─ close/update ticket
 └─ recompute frontier
 │
 ▼
Repeat until all tickets complete
 │
 ▼
Final feature verification
 │
 ▼
Fresh final AGY review
 │
 ▼
Feature complete
```

---

# 3. Planning Phase

## Step 1 — `grill-with-docs`

Bắt đầu feature bằng:

```text
/skill:grill-with-docs
```

hoặc command tương ứng mà OMP expose.

Mục tiêu:

- làm rõ problem;
- xác định expected behavior;
- làm rõ edge cases;
- xác định constraints;
- khóa những decision quan trọng;
- cập nhật domain knowledge hoặc ADR khi cần.

Nếu không muốn lưu domain documentation, có thể dùng:

```text
grill-me
```

thay cho `grill-with-docs`.

Tuy nhiên với development trong một repository lâu dài, ưu tiên:

```text
grill-with-docs
```

---

## Step 2 — `to-spec`

Sau khi requirements đủ rõ:

```text
/skill:to-spec
```

Spec là nguồn mô tả feature ở mức sản phẩm và kỹ thuật.

Spec nên trả lời:

- vấn đề cần giải quyết;
- desired behavior;
- important constraints;
- architecture decisions;
- testing decisions;
- out-of-scope;
- acceptance expectations.

Không bắt đầu implementation khi spec vẫn còn decision quan trọng chưa giải quyết.

---

## Step 3 — `to-tickets`

Sau khi spec được chấp nhận:

```text
/skill:to-tickets
```

Mục tiêu là chia spec thành các **vertical tracer-bullet tickets**.

Một ticket tốt nên có:

```text
Behavior
Acceptance criteria
Testing seam
Demo path
Dependencies / blockers
Parent spec
```

Không cần micro-manage implementation bằng exact file path hoặc line number nếu ticket đã đủ rõ về behavior.

Mỗi ticket phải đủ nhỏ để:

> một fresh AGY context có thể implement hoàn chỉnh.

---

# 4. User Approval Gate

Sau `to-tickets`, OMP không nên tự động bắt đầu coding ngay nếu user chưa duyệt ticket decomposition.

User review:

```text
spec
↓
tickets
↓
dependency graph
↓
scope
```

Sau khi được chấp nhận:

```text
Ship these tickets with AGY.
```

hoặc:

```text
/skill:ship-with-agy
```

Từ đây `ship-with-agy` sở hữu delivery orchestration.

---

# 5. Vai trò của OMP khi `ship-with-agy` chạy

OMP chuyển từ planner sang **conductor**.

OMP được phép:

```text
read tickets/spec
inspect tracker
inspect git
manage Herdr panes
start AGY agents
prompt AGY agents
run declared deterministic verification commands
collect evidence
evaluate acceptance gates
commit accepted work
update/close tickets
compute next frontier
```

OMP không được:

```text
edit product code
edit tests để sửa implementation
tự implement ticket
tự sửa bug
thay đổi requirement
tự redesign feature
```

Rule cốt lõi:

> OMP orchestrates implementation.
> OMP does not become the implementation worker.

---

# 6. Ticket Frontier

OMP đọc dependency graph và tìm các ticket hiện đang unblocked.

Ví dụ:

```text
       #101
      /    \
   #102    #103
      \    /
       #104
```

Ban đầu:

```text
frontier = #101
```

Sau khi `#101` hoàn thành:

```text
frontier = #102, #103
```

Version đầu của workflow vẫn xử lý sequential:

```text
#102
↓
#103
```

không chạy song song trong cùng checkout.

Sau khi cả hai hoàn thành:

```text
frontier = #104
```

---

# 7. One Ticket = One Fresh AGY

Mỗi ticket phải dùng một AGY implementation context mới.

Đúng:

```text
AGY-A → ticket #101
AGY-B → ticket #102
AGY-C → ticket #103
AGY-D → ticket #104
```

Không dùng:

```text
AGY-A
 ├─ ticket #101
 ├─ ticket #102
 ├─ ticket #103
 └─ ticket #104
```

Fresh context giúp:

- giảm context pollution;
- giảm assumption từ ticket trước;
- buộc ticket phải self-contained;
- giảm drift khỏi spec;
- review/debug dễ hơn.

---

# 8. Starting the AGY Implementer

OMP sử dụng Herdr để tạo một sibling pane mới.

Conceptually:

```text
OMP pane
 │
 ├─────────────┐
 │             │
 ▼             ▼
OMP        AGY implementer
```

AGY được start trong repository root hiện tại.

AGY worker nhận một self-contained brief gồm:

```text
role
ticket reference
parent spec
AGENTS.md
scope
acceptance criteria
testing seam
demo path
implementation restrictions
report contract
```

AGY phải đọc ticket và parent spec trước khi edit.

---

# 9. AGY Implementation Contract

AGY chịu trách nhiệm implementation cho đúng **một ticket**.

AGY phải:

```text
inspect codebase
↓
identify implementation seam
↓
implement behavior
↓
use TDD where appropriate
↓
run focused tests
↓
run declared self-verification
↓
report results
```

AGY không được:

```text
start another ticket
spawn additional workers
change requirements
expand scope
redesign settled decisions
commit
close ticket
invoke ship-with-agy
```

Implementation worker chỉ chịu trách nhiệm tạo candidate.

---

# 10. Remediation giữ cùng AGY context

Fresh context áp dụng giữa các ticket.

Nhưng nếu verifier tìm thấy defect trong **cùng ticket**, reuse implementation context đó.

Ví dụ:

```text
AGY-B
 │
 ├─ implement ticket #102
 │
 ▼
Verifier FAIL
 │
 ▼
OMP sends exact remediation delta
 │
 ▼
same AGY-B
 │
 ├─ reproduce
 ├─ diagnose
 ├─ fix
 └─ verify
```

Không tạo AGY mới cho mỗi lần sửa nhỏ của cùng ticket.

---

# 11. Freeze Candidate Before Verification

Khi AGY báo implementation hoàn tất, report của AGY chỉ là một claim.

OMP chưa được coi ticket là complete.

OMP tạo candidate fingerprint gồm những dữ liệu tương đương:

```text
HEAD
git status
staged diff
unstaged diff
untracked files
content hashes
```

Conceptually:

```text
implementation complete
        ↓
candidate C1
        ↓
verification
        ↓
candidate C2
```

Nếu:

```text
C1 != C2
```

thì verification bị invalidate.

Verdict phải là:

```text
CANDIDATE_CHANGED
```

chứ không phải PASS hay FAIL.

Điều này ngăn reviewer đánh giá một diff trong khi working tree đã thay đổi.

---

# 12. Verification có hai lớp

## Layer A — Deterministic Verification

OMP có thể chạy những command đã được project/ticket/spec xác định rõ.

Ví dụ:

```text
npm test
npm run lint
npm run typecheck
npm run build
```

OMP chỉ thực hiện và thu evidence:

```text
command
cwd
exit code
stdout/stderr
```

OMP không được tự invent verification command.

Command authority phải đến từ một trong:

```text
ticket
parent spec
AGENTS.md
README
project manifests/scripts
```

Nếu không có verification command đáng tin cậy:

```text
do not guess
```

---

## Layer B — Fresh AGY Verifier

Sau deterministic checks, OMP tạo:

```text
fresh AGY verifier
```

ở một Herdr pane mới.

Verifier chạy read-only / plan mode.

Verifier không nhận:

```text
implementer success claims
implementer self-justification
previous verifier verdict
```

Verifier chỉ nhận:

```text
ticket
parent spec
candidate working tree
acceptance criteria
demo path
verification evidence
```

Mục tiêu là giảm confirmation bias.

---

# 13. AGY Verifier Responsibilities

Verifier review các trục độc lập:

## Standards

Kiểm tra:

```text
correctness
code quality
architecture consistency
test integrity
unnecessary complexity
security/reliability concerns
```

## Ticket / Spec compliance

Kiểm tra:

```text
required behavior implemented
acceptance criteria satisfied
no scope shortfall
no scope creep
parent spec respected
```

## Test integrity

Đặc biệt kiểm tra:

```text
weakened assertions
skipped tests
disabled tests
deleted coverage
tests changed chỉ để làm suite pass
```

## Demo path

Verifier thực hiện đúng demo path của ticket nếu khả thi.

Không tự invent một smoke scenario hoàn toàn mới trừ khi ticket yêu cầu.

---

# 14. Verifier Verdict

Verifier kết thúc với một trong:

```text
PASS
FAIL
BLOCKED
```

Nhưng OMP còn phải classify failure.

---

# 15. Failure Classification

## `IMPLEMENTATION_DEFECT`

Ví dụ:

```text
test failure
incorrect behavior
missing edge case
broken integration
```

Action:

```text
same AGY implementer
↓
exact remediation prompt
↓
fresh verifier
```

---

## `SPEC_GAP`

Ví dụ:

```text
requirement ambiguous
ticket contradicts parent spec
important behavior undefined
architecture decision missing
```

Action:

```text
STOP
↓
return to OMP/user
```

Không cho implementation worker tự quyết product/design requirement.

---

## `ENVIRONMENT_BLOCKED`

Ví dụ:

```text
missing credentials
service unavailable
required dependency unavailable
test environment cannot start
```

Action:

```text
STOP
↓
user/environment intervention
```

---

## `PROTECTED_DECISION`

Bao gồm:

```text
credentials
destructive actions
permission bypass
deployment
publishing
scope expansion
requirement changes
architecture redesign
```

Action:

```text
STOP
↓
ask user
```

---

## `CANDIDATE_CHANGED`

Working tree thay đổi trong verification.

Action:

```text
discard verifier verdict
↓
re-establish stable candidate
↓
verify again
```

---

# 16. Bounded Remediation

Một ticket không được loop vô hạn.

Ví dụ policy:

```text
initial implementation
+
maximum 3 remediation rounds
```

Nếu cùng một blocker lặp lại mà không có measurable progress:

```text
STOP
```

và báo lại user.

---

# 17. Commit chỉ sau Independent PASS

AGY implementer không commit.

AGY verifier không commit.

Sau khi:

```text
deterministic verification = PASS
+
fresh verifier = PASS
+
candidate unchanged
+
zero blocking findings
```

OMP mới tạo Git checkpoint.

Conceptually:

```text
git add <accepted candidate>
git commit
```

Commit message/trailer phải chứa ticket reference.

Ví dụ:

```text
Add supplier search popup

Ticket: #102
Spec: #100
```

Commit trở thành durable proof:

```text
ticket #102
=
accepted implementation checkpoint
```

---

# 18. Tracker Update

Sau commit:

```text
commit SHA
↓
attach/update tracker
↓
close ticket
↓
re-read tracker state
```

Chỉ khi tracker xác nhận ticket đã complete thì OMP mới coi dependency được unblock.

Nếu tracker update fail:

```text
STOP
```

Không chạy ticket tiếp theo trên frontier giả.

---

# 19. Local Markdown Tickets

Nếu `to-tickets` dùng local Markdown:

```text
.scratch/feature/issues/
├── 01-foundation.md
├── 02-api.md
├── 03-ui.md
└── 04-integration.md
```

`ship-with-agy` không sửa các ticket file chỉ để thêm:

```text
[x]
status: done
progress
```

Thay vào đó Git history là completion ledger:

```text
Ticket: .scratch/feature/issues/02-api.md
```

Không tạo thêm:

```text
progress.md
delivery-state.json
tasks-state.md
```

nếu không thực sự cần.

---

# 20. Advance to Next Ticket

Sau successful commit và tracker completion:

```text
OMP
↓
re-read tracker
↓
recompute frontier
↓
select next ticket
↓
start NEW AGY
```

Chu kỳ lặp lại:

```text
ticket
→ fresh AGY
→ implementation
→ candidate freeze
→ deterministic checks
→ fresh verifier
→ acceptance
→ commit
→ close
→ next ticket
```

---

# 21. Final Feature Closeout

Ticket-level PASS chưa đủ để đảm bảo toàn feature đúng.

Sau khi tất cả tickets complete:

```text
feature base
      ↓
delivery-base..HEAD
      ↓
full project verification
      ↓
fresh final AGY verifier
      ↓
compare complete feature
against parent spec
```

Final verifier kiểm tra:

```text
cross-ticket integration
full spec compliance
regressions
architecture consistency
scope completeness
full demo behavior
```

---

# 22. Final Closeout Failure

Nếu final verifier tìm thấy defect rõ ràng thuộc ticket cụ thể:

```text
final review
↓
defect maps to ticket #103
↓
reopen/remediate ticket #103
↓
fresh AGY
↓
fix
↓
fresh verification
↓
follow-up commit
↓
run final closeout again
```

Giới hạn closeout remediation để tránh endless loop.

Ví dụ:

```text
maximum 2 final closeout remediation cycles
```

Nếu issue là spec gap hoặc architecture decision mới:

```text
STOP
↓
return to OMP/user
```

---

# 23. Herdr's Role

Herdr chỉ là runtime/orchestration layer.

Nó chịu trách nhiệm:

```text
pane lifecycle
agent lifecycle
prompt delivery
agent state
transcript inspection
agent wait
pane cleanup
```

Không dùng Herdr như planning system hoặc ticket tracker.

Architecture:

```text
                Herdr
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
      OMP      AGY Impl   AGY Verify
```

---

# 24. Pane Lifecycle

Một ticket có thể trông như:

```text
Tab
├── OMP conductor
├── AGY ticket implementer
└── AGY ticket verifier
```

Sau PASS:

```text
commit
↓
close workflow-created worker panes
↓
start next ticket with fresh panes
```

Nếu workflow FAIL/BLOCKED:

```text
preserve panes
preserve working tree
preserve transcript
```

để user inspection.

Không tự:

```text
git reset
git clean
git stash
```

user work.

---

# 25. Workflow State Machine

```text
PLANNING
   │
   ▼
SPEC_READY
   │
   ▼
TICKETS_READY
   │
   ▼
USER_APPROVED
   │
   ▼
COMPUTE_FRONTIER
   │
   ▼
DISPATCH_TICKET
   │
   ▼
IMPLEMENTING
   │
   ▼
CANDIDATE_FROZEN
   │
   ▼
VERIFYING
   │
   ├──────── FAIL ────────┐
   │                      │
   │                classify failure
   │                      │
   │           ┌──────────┼───────────┐
   │           ▼          ▼           ▼
   │        DEFECT     SPEC_GAP    BLOCKED
   │           │          │           │
   │      remediate      STOP        STOP
   │           │
   │           └──────────→ VERIFYING
   │
   ▼ PASS
COMMIT
   │
   ▼
CLOSE_TICKET
   │
   ▼
MORE_TICKETS?
   │
 ┌─┴─┐
 │YES│
 └─┬─┘
   │
   └────────→ COMPUTE_FRONTIER

 NO
 │
 ▼
FINAL_VERIFICATION
 │
 ▼
FINAL_REVIEW
 │
 ├─ FAIL → targeted remediation
 │
 ▼
COMPLETE
```

---

# 26. Responsibility Matrix

| Component           | Responsibility                                      |
| ------------------- | --------------------------------------------------- |
| User                | Product decisions, approval, protected decisions    |
| OMP                 | Discovery, architecture, spec, ticket decomposition |
| `grill-with-docs`   | Requirement discovery                               |
| `to-spec`           | Durable feature specification                       |
| `to-tickets`        | Vertical ticket decomposition                       |
| `ship-with-agy`     | Delivery orchestration                              |
| OMP conductor       | Frontier, dispatch, evidence, acceptance, commit    |
| Herdr               | Agent/pane lifecycle                                |
| AGY implementer     | Implement exactly one ticket                        |
| Matt TDD discipline | Implementation feedback loop                        |
| AGY verifier        | Independent qualitative review                      |
| Git                 | Accepted implementation checkpoints                 |
| GitHub/GitLab       | Ticket/dependency state                             |
| Parent spec         | Feature-level source of truth                       |

---

# 27. Core Rules

## Rule 1

```text
OMP plans and orchestrates.
AGY implements.
```

## Rule 2

```text
One ticket = one fresh AGY implementation context.
```

## Rule 3

```text
Reuse an implementer only for remediation of the same ticket.
```

## Rule 4

```text
Never trust the implementer's success report as completion evidence.
```

## Rule 5

```text
Every candidate receives fresh independent verification.
```

## Rule 6

```text
No ticket commit before verification PASS.
```

## Rule 7

```text
No next ticket before current ticket has a durable accepted checkpoint.
```

## Rule 8

```text
Implementation defects go back to the worker.
Requirement/design gaps go back to OMP/user.
```

## Rule 9

```text
No concurrent writers in the same checkout.
```

## Rule 10

```text
Do not create a second planning/state system around Matt Pocock tickets.
```

---

# 28. Recommended Daily Usage

For a normal feature:

```text
/skill:grill-with-docs
```

Discuss until requirements are clear.

Then:

```text
/skill:to-spec
```

Review the spec.

Then:

```text
/skill:to-tickets
```

Review ticket decomposition.

Then:

```text
/skill:ship-with-agy
```

OMP handles:

```text
ticket frontier
→ AGY
→ verification
→ remediation
→ commit
→ next ticket
→ final feature review
```

---

# 29. Final Architecture

```text
                    USER
                      │
                      ▼
                OMP
          planning / architecture
                      │
         ┌────────────┼────────────┐
         ▼            ▼            ▼
 grill-with-docs   to-spec     to-tickets
                                   │
                                   ▼
                            ship-with-agy
                                   │
                                   ▼
                           OMP CONDUCTOR
                                   │
                 ┌─────────────────┼─────────────────┐
                 │                 │                 │
                 ▼                 ▼                 ▼
              Herdr              Git             Tracker
                 │
          ┌──────┴──────┐
          ▼             ▼
    Fresh AGY       Fresh AGY
    Implementer      Verifier
          │             │
          └──────┬──────┘
                 ▼
             Acceptance
                 │
                 ▼
               Commit
                 │
                 ▼
            Next Ticket
                 │
                 ▼
        Final Feature Review
```

## Summary

Toàn bộ workflow có thể rút gọn thành:

```text
Understand
→ Specify
→ Slice
→ Approve
→ Dispatch
→ Implement
→ Freeze
→ Verify
→ Remediate
→ Commit
→ Advance
→ Integrate
→ Final Review
```

Hay theo tool:

```text
grill-with-docs
→ to-spec
→ to-tickets
→ ship-with-agy
    → fresh AGY per ticket
    → fresh verifier
    → commit
    → next ticket
→ final verification
```

Triết lý cốt lõi:

> **Matt Pocock Skills định nghĩa development lifecycle.
> OMP điều phối lifecycle.
> Herdr quản lý agent runtime.
> AGY thực hiện code.
> Independent verification quyết định candidate có được commit hay không.**
