def main():
    print("Hello from de-workshop!")


if __name__ == "__main__":
    main()
export GOOGLE_APPLICATION_CREDENTIALS="/Users/mac/Desktop/PERSONAL/secrets/organic-phoenix-484620-p3-2acea61335e2.json"
gcloud auth application-default set-quota-project organic-phoenix-484620-p3
terraform plan -var="project=organic-phoenix-484620-p3"