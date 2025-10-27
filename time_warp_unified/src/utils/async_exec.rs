/// Async execution support for Time Warp IDE

use anyhow::Result;
use tokio::sync::mpsc;
use std::sync::Arc;
use parking_lot::Mutex;

pub struct AsyncExecutor {
    runtime: tokio::runtime::Runtime,
}

impl AsyncExecutor {
    pub fn new() -> Result<Self> {
        let runtime = tokio::runtime::Builder::new_current_thread()
            .enable_all()
            .build()?;
        
        Ok(Self { runtime })
    }
    
    pub fn execute_async<F>(&self, code: String, mut callback: F) -> Result<()>
    where
        F: FnMut(ExecutionEvent) + Send + 'static,
    {
        let (tx, mut rx) = mpsc::channel(100);
        
        self.runtime.spawn(async move {
            let _ = tx.send(ExecutionEvent::Started).await;
            
            for (line_num, line) in code.lines().enumerate() {
                let _ = tx.send(ExecutionEvent::LineExecuted {
                    line_number: line_num + 1,
                    line: line.to_string(),
                }).await;
                
                tokio::time::sleep(tokio::time::Duration::from_millis(50)).await;
            }
            
            let _ = tx.send(ExecutionEvent::Completed).await;
        });
        
        self.runtime.spawn(async move {
            while let Some(event) = rx.recv().await {
                callback(event);
            }
        });
        
        Ok(())
    }
    
    pub fn execute_with_timeout(
        &self,
        code: String,
        timeout_ms: u64,
    ) -> Result<ExecutionResult> {
        self.runtime.block_on(async {
            let result = tokio::time::timeout(
                tokio::time::Duration::from_millis(timeout_ms),
                async { Self::execute_code_internal(code).await },
            ).await;
            
            match result {
                Ok(r) => r,
                Err(_) => Err(anyhow::anyhow!("Execution timeout")),
            }
        })
    }
    
    async fn execute_code_internal(code: String) -> Result<ExecutionResult> {
        Ok(ExecutionResult {
            output: vec![format!("Executed {} lines", code.lines().count())],
            variables: std::collections::HashMap::new(),
            execution_time_ms: 0,
        })
    }
}

impl Default for AsyncExecutor {
    fn default() -> Self {
        Self::new().expect("Failed to create async executor")
    }
}

#[derive(Debug, Clone)]
pub enum ExecutionEvent {
    Started,
    LineExecuted { line_number: usize, line: String },
    Output(String),
    Error(String),
    Completed,
}

#[derive(Debug, Clone)]
pub struct ExecutionResult {
    pub output: Vec<String>,
    pub variables: std::collections::HashMap<String, f64>,
    pub execution_time_ms: u64,
}

pub struct SharedExecutor {
    executor: Arc<Mutex<AsyncExecutor>>,
}

impl SharedExecutor {
    pub fn new() -> Result<Self> {
        Ok(Self {
            executor: Arc::new(Mutex::new(AsyncExecutor::new()?)),
        })
    }
    
    pub fn execute<F>(&self, code: String, callback: F) -> Result<()>
    where
        F: FnMut(ExecutionEvent) + Send + 'static,
    {
        self.executor.lock().execute_async(code, callback)
    }
}

impl Default for SharedExecutor {
    fn default() -> Self {
        Self::new().expect("Failed to create shared executor")
    }
}
