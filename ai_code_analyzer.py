"""
AI-POWERED LEGACY CODE ANALYZER
Demo for AI Consultant Interview

This tool demonstrates:
1. Security vulnerability detection
2. Code quality analysis
3. Automated refactoring suggestions
4. Migration recommendations

Usage:
    python ai_code_analyzer.py --file legacy_code_samples/order_service.py
    python ai_code_analyzer.py --file legacy_code_samples/order_service.py --refactor
    python ai_code_analyzer.py --dir legacy_code_samples/ --report
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check for API key
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

# Colored output for terminal
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_banner():
    """Print demo banner."""
    banner = f"""                          
                    """
    print(banner)


# ============================================================================
# SECURITY ANALYSIS
# ============================================================================

SECURITY_PROMPT = """You are a senior security engineer performing a security audit.

Analyze this code for security vulnerabilities:

```python
{code}
```

Identify ALL security issues including:
1. SQL Injection
2. Hardcoded credentials/secrets
3. Weak cryptography
4. Input validation issues
5. Information disclosure
6. Authentication flaws
7. Authorization issues

For EACH finding, provide:
- Severity: 🔴 CRITICAL, 🟠 HIGH, 🟡 MEDIUM, 🟢 LOW
- Line number(s)
- Vulnerability type
- Description
- Secure code fix

Format as a clear security report."""


# ============================================================================
# CODE QUALITY ANALYSIS
# ============================================================================

CODE_QUALITY_PROMPT = """You are a senior software architect reviewing legacy code for modernization.

Analyze this code for quality issues:

```python
{code}
```

Identify:
1. **Code Smells** - Long methods, god classes, magic numbers
2. **Outdated Patterns** - Callbacks that should be async/await, old string formatting
3. **Missing Best Practices** - No type hints, no docstrings, poor error handling
4. **SOLID Violations** - Single responsibility, dependency injection issues
5. **Testability Issues** - Tight coupling, no interfaces

For each issue:
- Location (line number)
- Issue type
- Why it's a problem
- Modern Python solution

Be specific and actionable."""


# ============================================================================
# REFACTORING
# ============================================================================

REFACTOR_PROMPT = """You are a Python modernization expert.

Refactor this legacy code to modern Python 3.11+ standards:

ORIGINAL CODE:
```python
{code}
```

Requirements:
1. Fix ALL security vulnerabilities (use parameterized queries, env vars for secrets)
2. Add type hints to all functions
3. Convert callbacks to async/await where applicable
4. Add proper error handling with specific exceptions
5. Add docstrings (Google style)
6. Break down god methods into smaller functions
7. Use dataclasses or Pydantic for data structures
8. Follow PEP 8

Output ONLY the refactored Python code, no explanations.
Include comments showing what was changed."""


# ============================================================================
# MIGRATION ANALYSIS
# ============================================================================

MIGRATION_PROMPT = """You are a technical lead planning a legacy code migration.

Analyze this codebase for migration to modern architecture:

```python
{code}
```

Provide a migration plan including:

## 1. Current State Assessment
- Tech debt items
- Risk areas
- Dependencies

## 2. Target Architecture
- Recommended patterns (Repository, Service Layer, etc.)
- Framework recommendations (FastAPI, SQLAlchemy, etc.)
- Testing strategy

## 3. Migration Phases
- Phase 1: Quick wins (what can be fixed immediately)
- Phase 2: Refactoring (structural changes)
- Phase 3: Modernization (new patterns/frameworks)

## 4. Effort Estimation
- Small (1-2 days)
- Medium (1 week)
- Large (2+ weeks)

## 5. Risk Mitigation
- How to migrate safely without breaking production

Be specific to THIS codebase."""



class AICodeAnalyzer:
    """AI-powered code analysis tool."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with OpenAI API."""
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        
        if not self.api_key:
            print(f"{Colors.YELLOW}  No OPENAI_API_KEY found. Running in DEMO mode with sample outputs.{Colors.END}")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)
            print(f"{Colors.GREEN}✓ Connected to OpenAI API{Colors.END}")
    
    def _call_ai(self, prompt: str) -> str:
        """Call OpenAI API or return demo response."""
        
        if self.client:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        else:
            # Demo mode - return pre-built response
            return self._get_demo_response(prompt)
    
    def _get_demo_response(self, prompt: str) -> str:
        """Return demo responses when no API key."""
        prompt_lower = prompt.lower()
        
        if "refactor" in prompt_lower or "modern python" in prompt_lower:
            return DEMO_REFACTOR_RESPONSE
        elif "migration" in prompt_lower or "migration plan" in prompt_lower:
            return DEMO_MIGRATION_RESPONSE
        elif "security" in prompt_lower or "vulnerabilities" in prompt_lower:
            return DEMO_SECURITY_RESPONSE
        elif "quality" in prompt_lower or "code smells" in prompt_lower:
            return DEMO_QUALITY_RESPONSE
        return "Demo response"
    
    def analyze_security(self, code: str) -> str:
        """Run security analysis."""
        print(f"\n{Colors.BOLD}🔒 Running Security Analysis...{Colors.END}\n")
        return self._call_ai(SECURITY_PROMPT.format(code=code))
    
    def analyze_quality(self, code: str) -> str:
        """Run code quality analysis."""
        print(f"\n{Colors.BOLD}📊 Running Code Quality Analysis...{Colors.END}\n")
        return self._call_ai(CODE_QUALITY_PROMPT.format(code=code))
    
    def refactor_code(self, code: str) -> str:
        """Generate refactored version."""
        print(f"\n{Colors.BOLD}🔧 Generating Refactored Code...{Colors.END}\n")
        return self._call_ai(REFACTOR_PROMPT.format(code=code))
    
    def migration_plan(self, code: str) -> str:
        """Generate migration plan."""
        print(f"\n{Colors.BOLD}📋 Generating Migration Plan...{Colors.END}\n")
        return self._call_ai(MIGRATION_PROMPT.format(code=code))
    
    def full_analysis(self, code: str, filename: str) -> str:
        """Run complete analysis pipeline."""
        
        report = []
        report.append(f"\n{'='*70}")
        report.append(f"FULL ANALYSIS REPORT: {filename}")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"{'='*70}\n")
        
        # Security
        report.append("\n" + "="*70)
        report.append("SECTION 1: SECURITY VULNERABILITIES")
        report.append("="*70)
        report.append(self.analyze_security(code))
        
        # Quality
        report.append("\n" + "="*70)
        report.append("SECTION 2: CODE QUALITY ISSUES")
        report.append("="*70)
        report.append(self.analyze_quality(code))
        
        # Migration
        report.append("\n" + "="*70)
        report.append("SECTION 3: MIGRATION RECOMMENDATIONS")
        report.append("="*70)
        report.append(self.migration_plan(code))
        
        return "\n".join(report)


# ============================================================================
# DEMO RESPONSES (Used when no API key)
# ============================================================================

DEMO_SECURITY_RESPONSE = """
## 🔒 Security Vulnerability Report

### 🔴 CRITICAL - SQL Injection (Lines 26-28, 33-35)
**Vulnerability:** User input directly concatenated into SQL queries
```python
# VULNERABLE (Line 27):
query = "SELECT * FROM orders WHERE id = '" + order_id + "'"

# VULNERABLE (Line 34):
query = f"SELECT * FROM orders WHERE customer_name LIKE '%{customer_name}%'"
```
**Attack:** `order_id = "'; DROP TABLE orders; --"`
**Fix:**
```python
query = "SELECT * FROM orders WHERE id = %s"
cursor.execute(query, (order_id,))
```

### 🔴 CRITICAL - Hardcoded Credentials (Lines 12-14)
**Vulnerability:** Database credentials and API keys in source code
```python
DB_PASSWORD = "admin123"  # Exposed in git history!
API_KEY = "sk-1234567890abcdef"  # Leaked API key
```
**Fix:**
```python
import os
DB_PASSWORD = os.environ.get("DB_PASSWORD")
API_KEY = os.environ.get("API_KEY")
```

### 🟠 HIGH - Hardcoded SMTP Credentials (Line 78)
**Vulnerability:** Email password hardcoded in function
```python
server.login("reports@company.com", "reportpass123")
```

### 🟡 MEDIUM - No Input Validation (Line 40)
**Vulnerability:** `create_order()` accepts any data without validation
**Risk:** Invalid data, type errors, business logic bypass
**Fix:** Use Pydantic models for validation

---
**Summary:** 3 Critical, 1 High, 1 Medium vulnerabilities found
**Recommendation:** Block deployment until Critical issues are fixed
"""

DEMO_QUALITY_RESPONSE = """
## 📊 Code Quality Analysis

### Code Smells Detected:

**1. God Method (Lines 54-88) - `generate_report()`**
- Takes 7 parameters (should be max 3-4)
- Does 5 different things: query, format, email
- 35 lines long
- **Fix:** Split into `query_data()`, `format_report()`, `send_email()`

**2. Callback Hell (Lines 44-52) - `process_order()`**
- Nested callbacks 4 levels deep
- Hard to read and debug
- **Fix:** Convert to async/await:
```python
async def process_order(self, order_id: str) -> bool:
    order = await self.get_order(order_id)
    if not order:
        return False
    
    if not await self.validate_inventory(order):
        return False
    
    await self.charge_payment(order)
    await self.ship_order(order)
    return True
```

**3. Magic Numbers (Lines 97-104) - `calculate_shipping()`**
- Hardcoded values: 1, 5, 10, 5.99, 9.99, 14.99, 19.99, 0.50
- **Fix:** Use constants or config:
```python
SHIPPING_RATES = {
    "light": {"max_weight": 1, "cost": 5.99},
    "medium": {"max_weight": 5, "cost": 9.99},
    "heavy": {"max_weight": 10, "cost": 14.99},
    "extra_per_lb": 0.50
}
```

**4. Missing Type Hints (Entire file)**
- No function has type annotations
- Makes IDE support and refactoring harder

**5. No Error Handling**
- Database operations have no try/except
- Connection failures will crash the app

---
**Technical Debt Score:** 7/10 (High)
**Recommended Action:** Refactor before adding new features
"""

DEMO_REFACTOR_RESPONSE = '''"""
REFACTORED ORDER SERVICE
Modern Python 3.11+ with security fixes and best practices
"""

import os
from dataclasses import dataclass
from typing import Optional
from enum import Enum
import mysql.connector
from mysql.connector import Error as MySQLError


# Configuration from environment variables (SECURITY FIX)
@dataclass
class DatabaseConfig:
    """Database configuration from environment."""
    host: str = os.environ.get("DB_HOST", "localhost")
    user: str = os.environ.get("DB_USER", "")
    password: str = os.environ.get("DB_PASSWORD", "")
    database: str = os.environ.get("DB_NAME", "ecommerce")


@dataclass
class OrderData:
    """Validated order data structure."""
    customer_id: int
    product_id: int
    quantity: int
    total: float
    
    def __post_init__(self):
        """Validate order data."""
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.total < 0:
            raise ValueError("Total cannot be negative")


class OrderService:
    """Modern order service with security and quality improvements."""
    
    def __init__(self, config: Optional[DatabaseConfig] = None):
        """Initialize with database configuration.
        
        Args:
            config: Database configuration. Uses env vars if not provided.
        """
        self.config = config or DatabaseConfig()
        self._connection = None
    
    @property
    def connection(self):
        """Lazy database connection with error handling."""
        if self._connection is None or not self._connection.is_connected():
            try:
                self._connection = mysql.connector.connect(
                    host=self.config.host,
                    user=self.config.user,
                    password=self.config.password,
                    database=self.config.database
                )
            except MySQLError as e:
                raise ConnectionError(f"Database connection failed: {e}")
        return self._connection
    
    def get_order(self, order_id: int) -> Optional[dict]:
        """Get order by ID using parameterized query.
        
        Args:
            order_id: The order ID to retrieve.
            
        Returns:
            Order dict or None if not found.
            
        Raises:
            ValueError: If order_id is invalid.
        """
        if not isinstance(order_id, int) or order_id <= 0:
            raise ValueError("order_id must be a positive integer")
        
        # SECURITY FIX: Parameterized query prevents SQL injection
        query = "SELECT * FROM orders WHERE id = %s"
        
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, (order_id,))
                return cursor.fetchone()
        except MySQLError as e:
            raise RuntimeError(f"Database query failed: {e}")
    
    def search_orders(self, customer_name: str) -> list[dict]:
        """Search orders by customer name safely.
        
        Args:
            customer_name: Name to search for (partial match).
            
        Returns:
            List of matching orders.
        """
        # SECURITY FIX: Parameterized LIKE query
        query = "SELECT * FROM orders WHERE customer_name LIKE %s"
        search_pattern = f"%{customer_name}%"
        
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, (search_pattern,))
                return cursor.fetchall()
        except MySQLError as e:
            raise RuntimeError(f"Search failed: {e}")
    
    def create_order(self, order: OrderData) -> int:
        """Create a new order with validation.
        
        Args:
            order: Validated order data.
            
        Returns:
            New order ID.
        """
        query = """
            INSERT INTO orders (customer_id, product_id, quantity, total) 
            VALUES (%s, %s, %s, %s)
        """
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (
                    order.customer_id,
                    order.product_id,
                    order.quantity,
                    order.total
                ))
                self.connection.commit()
                return cursor.lastrowid
        except MySQLError as e:
            self.connection.rollback()
            raise RuntimeError(f"Order creation failed: {e}")
    
    async def process_order(self, order_id: int) -> bool:
        """Process order with async/await (REFACTORED from callbacks).
        
        Args:
            order_id: Order to process.
            
        Returns:
            True if successful, False otherwise.
        """
        order = self.get_order(order_id)
        if not order:
            return False
        
        # Clean async flow instead of callback hell
        if not await self._validate_inventory(order):
            return False
        
        if not await self._charge_payment(order):
            return False
        
        return await self._ship_order(order)
    
    async def _validate_inventory(self, order: dict) -> bool:
        """Validate inventory availability."""
        # Implementation here
        return True
    
    async def _charge_payment(self, order: dict) -> bool:
        """Process payment."""
        # Implementation here
        return True
    
    async def _ship_order(self, order: dict) -> bool:
        """Initiate shipping."""
        # Implementation here
        return True


# REFACTORED: Constants instead of magic numbers
class ShippingTier(Enum):
    """Shipping cost tiers."""
    LIGHT = (1, 5.99)
    MEDIUM = (5, 9.99)
    HEAVY = (10, 14.99)
    EXTRA_PER_LB = 0.50


def calculate_shipping(weight: float) -> float:
    """Calculate shipping cost based on weight.
    
    Args:
        weight: Package weight in pounds.
        
    Returns:
        Shipping cost in dollars.
    """
    if weight < ShippingTier.LIGHT.value[0]:
        return ShippingTier.LIGHT.value[1]
    elif weight < ShippingTier.MEDIUM.value[0]:
        return ShippingTier.MEDIUM.value[1]
    elif weight < ShippingTier.HEAVY.value[0]:
        return ShippingTier.HEAVY.value[1]
    else:
        base = ShippingTier.HEAVY.value[1]
        extra_weight = weight - ShippingTier.HEAVY.value[0]
        return base + (extra_weight * ShippingTier.EXTRA_PER_LB.value)


def format_price(amount: float) -> str:
    """Format amount as currency string.
    
    Args:
        amount: Dollar amount.
        
    Returns:
        Formatted price string.
    """
    # REFACTORED: f-string instead of % formatting
    return f"${amount:.2f}"
'''

DEMO_MIGRATION_RESPONSE = """
## 📋 Migration Plan: Order Service Modernization

### 1. Current State Assessment

**Tech Debt Items:**
| Item | Severity | Effort |
|------|----------|--------|
| SQL Injection vulnerabilities | Critical | Small |
| Hardcoded credentials | Critical | Small |
| No input validation | High | Medium |
| Callback-based async | Medium | Medium |
| No type hints | Low | Small |
| God methods | Medium | Medium |

**Risk Areas:**
- Payment processing code (highest business risk)
- Customer data handling (compliance risk)
- Report generation (performance risk)

### 2. Target Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      API Layer (FastAPI)                     │
├─────────────────────────────────────────────────────────────┤
│                    Service Layer                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │OrderService │  │PaymentSvc   │  │ShippingSvc  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│                  Repository Layer (SQLAlchemy)               │
├─────────────────────────────────────────────────────────────┤
│                      Database (MySQL)                        │
└─────────────────────────────────────────────────────────────┘
```

**Recommended Stack:**
- FastAPI (async support, auto-docs)
- SQLAlchemy 2.0 (type-safe ORM)
- Pydantic (validation)
- pytest + pytest-asyncio (testing)

### 3. Migration Phases

**Phase 1: Security Fixes (Week 1)** ✅ Quick Win
- [ ] Replace string concatenation with parameterized queries
- [ ] Move credentials to environment variables
- [ ] Add input validation with Pydantic
- **No architectural changes - just fixes**

**Phase 2: Code Quality (Week 2-3)**
- [ ] Add type hints to all functions
- [ ] Break down god methods
- [ ] Convert callbacks to async/await
- [ ] Add error handling
- [ ] Add unit tests for existing behavior

**Phase 3: Architecture Modernization (Week 4-6)**
- [ ] Introduce Repository pattern
- [ ] Add Service layer abstraction
- [ ] Migrate to FastAPI endpoints
- [ ] Add integration tests
- [ ] Set up CI/CD pipeline

### 4. Effort Estimation

| Task | Effort | Priority |
|------|--------|----------|
| Fix SQL injection | 2 hours | P0 |
| Move credentials to env | 1 hour | P0 |
| Add Pydantic validation | 4 hours | P1 |
| Add type hints | 2 hours | P2 |
| Refactor god methods | 8 hours | P2 |
| Convert to async | 4 hours | P2 |
| Add Repository layer | 16 hours | P3 |
| Migrate to FastAPI | 24 hours | P3 |

**Total: ~60 hours (1.5 developer-weeks)**

### 5. Risk Mitigation

**Safe Migration Strategy:**
1. **Add tests FIRST** - Before changing anything, add tests for current behavior
2. **Feature flags** - Use flags to switch between old/new code
3. **Strangler pattern** - New code wraps old code, gradually replace
4. **Shadow mode** - Run new code alongside old, compare results
5. **Rollback plan** - Keep old code deployable for 2 weeks after migration

**Monitoring:**
- Add logging to track old vs new code paths
- Alert on any discrepancies
- Track error rates during migration
"""


# ============================================================================
# MAIN CLI
# ============================================================================

def main():
    """Main entry point."""
    print_banner()
    
    parser = argparse.ArgumentParser(description="AI-Powered Legacy Code Analyzer")
    parser.add_argument("--file", "-f", help="Python file to analyze")
    parser.add_argument("--dir", "-d", help="Directory to analyze")
    parser.add_argument("--security", action="store_true", help="Run security analysis only")
    parser.add_argument("--quality", action="store_true", help="Run quality analysis only")
    parser.add_argument("--refactor", action="store_true", help="Generate refactored code")
    parser.add_argument("--migrate", action="store_true", help="Generate migration plan")
    parser.add_argument("--full", action="store_true", help="Run full analysis")
    parser.add_argument("--output", "-o", help="Output file for report")
    
    args = parser.parse_args()
    
    # Default to showing help with sample command
    if not args.file and not args.dir:
        print(f"{Colors.YELLOW}Usage Examples:{Colors.END}")
        print(f"  python ai_code_analyzer.py --file legacy_code_samples/order_service.py --security")
        print(f"  python ai_code_analyzer.py --file legacy_code_samples/order_service.py --refactor")
        print(f"  python ai_code_analyzer.py --file legacy_code_samples/order_service.py --full")
        print(f"  python ai_code_analyzer.py --dir legacy_code_samples/ --full --output report.md")
        print()
        
        # Run demo with sample file
        demo_file = Path(__file__).parent / "legacy_code_samples" / "order_service.py"
        if demo_file.exists():
            print(f"{Colors.CYAN}Running demo with sample file...{Colors.END}")
            args.file = str(demo_file)
            args.full = True
    
    analyzer = AICodeAnalyzer()
    
    if args.file:
        filepath = Path(args.file)
        if not filepath.exists():
            print(f"{Colors.RED}Error: File not found: {args.file}{Colors.END}")
            sys.exit(1)
        
        code = filepath.read_text()
        print(f"\n{Colors.CYAN}Analyzing: {filepath.name}{Colors.END}")
        print(f"Lines of code: {len(code.splitlines())}")
        
        output = ""
        
        if args.security:
            output = analyzer.analyze_security(code)
        elif args.quality:
            output = analyzer.analyze_quality(code)
        elif args.refactor:
            output = analyzer.refactor_code(code)
        elif args.migrate:
            output = analyzer.migration_plan(code)
        elif args.full:
            output = analyzer.full_analysis(code, filepath.name)
        else:
            # Default to security
            output = analyzer.analyze_security(code)
        
        print(output)
        
        if args.output:
            Path(args.output).write_text(output)
            print(f"\n{Colors.GREEN}✓ Report saved to: {args.output}{Colors.END}")
    
    elif args.dir:
        dirpath = Path(args.dir)
        if not dirpath.exists():
            print(f"{Colors.RED}Error: Directory not found: {args.dir}{Colors.END}")
            sys.exit(1)
        
        # Analyze all Python files
        reports = []
        for pyfile in dirpath.glob("**/*.py"):
            code = pyfile.read_text()
            print(f"\n{Colors.CYAN}Analyzing: {pyfile.name}{Colors.END}")
            report = analyzer.full_analysis(code, pyfile.name)
            reports.append(report)
        
        full_report = "\n\n".join(reports)
        print(full_report)
        
        if args.output:
            Path(args.output).write_text(full_report)
            print(f"\n{Colors.GREEN}✓ Report saved to: {args.output}{Colors.END}")


if __name__ == "__main__":
    main()
