Here’s your content formatted in clean and structured **Markdown**:

---

# 📢 Logging & Progress Notifications in MCP

## 📝 Summary

**Logging and progress notifications** are simple to implement but significantly improve user experience in **MCP servers**.
They keep users informed about long-running operations, preventing confusion or the assumption that something is broken.

When Claude calls a tool that takes time (e.g., researching or processing data), users typically see **no output** until it finishes.
This can be **frustrating** as they have no idea if the process is still running or has stalled.

With **logging and progress notifications**, users get **real-time feedback**:
✅ Progress bars
✅ Status messages
✅ Detailed logs
...all while the tool is still running.

---

## ⚙️ How It Works

In the Python **MCP SDK**, logging and progress work via the `Context` object automatically passed to your tool functions.
This `context` object provides methods to send **log messages** and **progress updates** to the client.

### 🧪 Example Tool

```python
@mcp.tool(
    name="research",
    description="Research a given topic"
)
async def research(
    topic: str = Field(description="Topic to research"),
    *,
    context: Context
):
    await context.info("About to do research...")
    await context.report_progress(20, 100)
    
    sources = await do_research(topic)
    
    await context.info("Writing report...")
    await context.report_progress(70, 100)
    
    results = await generate_report(sources)
    
    return results
```

### 🛠️ Key Context Methods

* `context.info(message: str)`
  → Sends **log messages** to the client.

* `context.report_progress(current: float, total: float)`
  → Sends **progress updates** (e.g., `20 / 100`).

---

## 👨‍💻 Client-Side Implementation

On the client, define **callbacks** to handle logging and progress notifications:

### 🔍 Logging Callback

```python
async def logging_callback(params: LoggingMessageNotificationParams):
    print(params.data)
```

### 📈 Progress Callback

```python
async def print_progress_callback(
    progress: float, total: float | None, message: str | None
):
    if total is not None:
        percentage = (progress / total) * 100
        print(f"Progress: {progress}/{total} ({percentage:.1f}%)")
    else:
        print(f"Progress: {progress}")
```

### 🚀 Running with Client Session

```python
async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read,
            write,
            logging_callback=logging_callback
        ) as session:
            await session.initialize()
            
            await session.call_tool(
                name="add",
                arguments={"a": 1, "b": 3},
                progress_callback=print_progress_callback,
            )
```

* Pass `logging_callback` during **session initialization**
* Pass `progress_callback` during **tool call execution**

---

## 🧑‍🎨 Presentation Options

How you show logs and progress depends on your app type:

| Application Type | Notification Presentation                   |
| ---------------- | ------------------------------------------- |
| **CLI**          | Print messages and progress in the terminal |
| **Web**          | Use WebSockets, SSE, or polling for updates |
| **Desktop**      | Update UI components like progress bars     |

---

## 💡 Final Notes

* **Optional Feature:** You can skip notifications if not needed.
* **Customizable UX:** Show only relevant messages or format them your way.
* **Improves Clarity:** Keeps users engaged during long-running tools.

> 🧠 *Good UX = Clear Feedback*

---

Remember that implementing these notifications is entirely optional. You can choose to ignore them completely, show only certain types, or present them however makes sense for your application. They're purely user experience enhancements to help users understand what's happening during long-running operations.