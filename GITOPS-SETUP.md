# TropoMetrics GitOps Deployment Guide for Portainer + k3s

## 🎯 **Complete GitOps Setup**

This guide shows how to configure automatic redeployment when commits are made to your branches.

## 📋 **Current Environment Configuration**

| Environment | Branch | Namespace | Port | Image Tag |
|-------------|--------|-----------|------|-----------|
| Production | `main` | `tropometrics` | 30080 | `:main` |
| Development | `dev` | `tropometrics` | 30082 | `:dev` |
| Testing | `test` | `tropometrics` | 30081 | `:test` |

## 🚀 **Step 1: Portainer Application Setup**

### **For Each Environment (main, dev, test):**

1. **Go to Portainer** → **Applications** → **Create Application**
2. **Select**: "Create from Git repository" 
3. **Configure**:
   - **Name**: `tropometrics-main` (or dev/test)
   - **Repository URL**: `https://github.com/TomTheLEGEND23/HHS-TropoMetrics`
   - **Reference**: `refs/heads/main` (or dev/test)
   - **Manifest Path**: `k8s/portainer-main.yaml` (or dev/test)
   - **Enable Auto-update**: ✅ **YES**
   - **Fetch interval**: `30s` (or your preference)

4. **Authentication** (if needed):
   - For public repos: No auth needed
   - For private repos: Add GitHub credentials

### **Alternative: Use Portainer Stacks**

1. **Go to Portainer** → **Stacks** → **Add Stack**
2. **Select**: "Git Repository"
3. **Configure**:
   - **Name**: `tropometrics-main`
   - **Repository URL**: `https://github.com/TomTheLEGEND23/HHS-TropoMetrics`
   - **Reference**: `main`
   - **Compose file path**: `k8s/portainer-main.yaml`
   - **Auto-update**: ✅ Enable
   - **Webhook**: ✅ Enable (optional for faster updates)

## 🔄 **Step 2: GitOps Workflow**

### **How Auto-Updates Work:**

1. **Developer pushes** code to branch (`main`, `dev`, `test`)
2. **GitHub Actions** builds and pushes new Docker image
3. **Portainer detects** Git repository changes (every 30s)
4. **Portainer pulls** updated manifest files
5. **k3s applies** changes with `imagePullPolicy: Always`
6. **Rolling update** deploys new containers
7. **Zero downtime** deployment completed

### **Update Flow:**
```
Code Push → GitHub Actions → New Image → Portainer GitOps → k3s Deployment
     ↓            ↓            ↓            ↓              ↓
   Commit     Build Image   Push to      Pull Git       Apply YAML
              Tag :main     Registry     Changes        Rolling Update
```

## ⚡ **Step 3: Faster Updates with Webhooks**

### **Option A: Portainer Webhooks**

1. **In Portainer Stack** → **Webhooks** → **Create Webhook**
2. **Copy webhook URL**
3. **Add to GitHub** → **Settings** → **Webhooks** → **Add webhook**
4. **Paste URL** and set **Content type**: `application/json`
5. **Events**: Select "Just the push event"

### **Option B: Enhanced GitHub Actions**

Add webhook trigger to your workflow:

```yaml
- name: Trigger Portainer Update
  if: github.event_name == 'push'
  run: |
    if [ -n "${{ secrets.PORTAINER_WEBHOOK_MAIN }}" ] && [ "${{ github.ref }}" == "refs/heads/main" ]; then
      curl -X POST "${{ secrets.PORTAINER_WEBHOOK_MAIN }}"
    fi
    if [ -n "${{ secrets.PORTAINER_WEBHOOK_DEV }}" ] && [ "${{ github.ref }}" == "refs/heads/dev" ]; then
      curl -X POST "${{ secrets.PORTAINER_WEBHOOK_DEV }}"  
    fi
    if [ -n "${{ secrets.PORTAINER_WEBHOOK_TEST }}" ] && [ "${{ github.ref }}" == "refs/heads/test" ]; then
      curl -X POST "${{ secrets.PORTAINER_WEBHOOK_TEST }}"
    fi
```

## 🔧 **Step 4: Verification**

### **Test GitOps Deployment:**

1. **Make a change** to `Website/index.html`
2. **Commit and push** to `dev` branch
3. **Check GitHub Actions**: Should build `:dev` image
4. **Check Portainer**: Should detect changes and redeploy
5. **Verify deployment**: `http://NODE_IP:30082`

### **Monitoring Commands:**

```bash
# Check deployment status
kubectl get deployments -n tropometrics

# Watch pods rolling update
kubectl get pods -n tropometrics -w

# Check application logs
kubectl logs -n tropometrics -l environment=development

# Verify image tags
kubectl get pods -n tropometrics -o jsonpath='{.items[*].spec.containers[*].image}'
```

## 📊 **Step 5: Environment Access**

After setup, your environments will be accessible at:

- **🏭 Production**: `http://NODE_IP:30080` (main branch)
- **🔧 Development**: `http://NODE_IP:30082` (dev branch)  
- **🧪 Testing**: `http://NODE_IP:30081` (test branch)

## ⚠️ **Important Notes**

### **Resource Considerations:**
- **Production**: Auto-scaling 3-12 pods based on CPU
- **Dev/Test**: Single pod deployments
- **Same namespace**: All environments use `tropometrics`

### **GitOps Best Practices:**
- ✅ **Separate manifests** per environment
- ✅ **Branch-specific images** (`:main`, `:dev`, `:test`)
- ✅ **Rolling updates** with health checks
- ✅ **Auto-pull latest** images
- ✅ **Monitor deployment** progress

## 🎯 **Quick Setup Summary**

1. **Create 3 Portainer Applications** (one per environment)
2. **Point each to same Git repo** but different branches/manifests
3. **Enable auto-update** with 30s interval
4. **Set up webhooks** for instant updates (optional)
5. **Test the workflow** by making commits

Your GitOps setup will now automatically deploy changes when you commit to any branch! 🚀