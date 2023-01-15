import pulumi
import pulumi_docker as docker
import pulumi_azure_native.resources as resources
import pulumi_azure_native.web as web

config = pulumi.Config()

dockerHubUserName = config.require("username")
dockerHubPassword = config.require("password")
imageName = "flask_azure_pulumi"
imageTag = "v1.0.0"  # Change to whatever version you are creating
azureResourceLocation = (
    "UAE North"  # Change to the region that is closest to your end users
)

flaskAzureImage = docker.Image(
    imageName,
    build=docker.DockerBuild(context="app"),
    image_name=f"{dockerHubUserName}/{imageName}:{imageTag}",
    registry=docker.ImageRegistry(
        server="docker.io", username=dockerHubUserName, password=dockerHubPassword
    ),
)

resource_group = resources.ResourceGroup(
    "pulumi_flask_app", location=azureResourceLocation
)

plan = web.AppServicePlan(
    "pulumi",
    resource_group_name=resource_group.name,
    kind="Linux",
    location=azureResourceLocation,
    reserved=True,
    sku=web.SkuDescriptionArgs(
        name="F1",
        tier="Free",
    ),
)

flask_alpine = web.WebApp(
    "flask-azure-pulumi",
    resource_group_name=resource_group.name,
    server_farm_id=plan.id,
    site_config=web.SiteConfigArgs(
        app_settings=[
            web.NameValuePairArgs(
                name="WEBSITES_ENABLE_APP_SERVICE_STORAGE", value="false"
            )
        ],
        linux_fx_version=f"DOCKER|{dockerHubUserName}/{imageName}:{imageTag}",
    ),
    https_only=True,
)

pulumi.export(
    "websiteURL",
    flask_alpine.default_host_name.apply(
        lambda default_host_name: f"https://{default_host_name}"
    ),
)
